#!/usr/bin/env python3
"""
Deploy Stitch exports at the site document root (no /stitch-pages/ prefix).

- Each folder with code.html → /<slug>/index.html (+ image assets)
- Home export also written to /index.html
- `appointments/` is a static landing so /appointments/index.html wins over WordPress
  (otherwise the theme header appears on that URL).
- Prepends DirectoryIndex so index.html wins over index.php on /
- Removes remote stitch-pages/ tree if present

Local layout: slug folders live as direct children of your export root, each with code.html.

Before every deploy, run:
  python3 prepare_site_deploy.py

After deploy, confirm production updated:
  python3 verify_live_deploy.py

Defaults:
  Deploy root = the directory that contains this script (your repo root).
  Homepage folder = auto-detected (see resolve_home_slug).

Env overrides:
  WOA_DEPLOY_SOURCE       — Root folder that contains slug subfolders (overrides default above)
  WOA_HOME_SLUG           — Exact folder name for the homepage export (if auto-detect fails)
  WOA_ROOT_MEDIA_FOLDER   — Where loose images at repo root go (default: _repo_media)
  FTP_USER, FTP_PASS      — Required (never commit credentials into this file)

Child folders without code.html still upload when they contain image files in that folder
(non-recursive). Loose image files at repo root upload to /WOA_ROOT_MEDIA_FOLDER/.
`artists_build/*.html` deploys to `/artists/<name>/index.html` (e.g. katelyn-cole).

"""

from __future__ import annotations

import os
import sys
from ftplib import FTP, error_perm
from io import BytesIO
from pathlib import Path

from woa_ai_crawl import GEO_SLUG, SITEMAP_STATIC_NAME, write_ai_crawl_assets

_SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_CRAWL_FILES = ("llms.txt", "ai.txt", "robots.txt", "sitemap-static-pages.xml", "sitemap.xml")
_DEFAULT_SOURCE_ROOT = str(_SCRIPT_DIR)

SOURCES = [
    Path(os.environ.get("WOA_DEPLOY_SOURCE", _DEFAULT_SOURCE_ROOT)).expanduser().resolve()
]
HOST = "ftp.workofarttattoo.com"
_DEFAULT_HOME_SLUG = "home_work_of_art_tattoo_piercing"
LEGACY_PREFIX = "stitch-pages"


def resolve_home_slug(merged: dict[str, Path]) -> str | None:
    """
    Pick which subfolder supplies /index.html. Export folder names vary:
    home_work_of_art_tattoo_piercing vs home_work_of_art_tattoo, etc.
    """
    env = os.environ.get("WOA_HOME_SLUG", "").strip()
    candidates: list[str] = []
    if env:
        candidates.append(env)
    candidates.extend(
        [
            _DEFAULT_HOME_SLUG,
            "home_work_of_art_tattoo",
            "home_work_of_art",
        ]
    )
    seen: set[str] = set()
    for slug in candidates:
        if not slug or slug in seen:
            continue
        seen.add(slug)
        if slug in merged and (merged[slug] / "code.html").is_file():
            return slug

    prefixes = ("home_work_of_art", "home_")
    for name, path in sorted(merged.items()):
        if not any(name.startswith(p) for p in prefixes):
            continue
        if (path / "code.html").is_file():
            return name
    return None


IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico"}
# Non-HTML assets deployed beside index.html in each slug folder
SLUG_ASSET_EXT = IMAGE_EXT | {".css"}

SKIP_MEDIA_ONLY_NAMES = frozenset({"__pycache__", "node_modules"})


def iter_image_files_direct(local_dir: Path) -> list[Path]:
    """Image files directly inside local_dir (not in subfolders)."""
    return [
        p
        for p in sorted(local_dir.iterdir())
        if p.is_file() and p.suffix.lower() in IMAGE_EXT
    ]


def artist_remote_slug_from_folder(folder_name: str) -> str | None:
    """Map long Stitch folder names to /artists/<slug> paths."""
    lower = folder_name.lower()
    if "katelyn" in lower or "katie" in lower:
        return "katelyn-cole"
    if "joshua" in lower:
        return "joshua-cole"
    return None


def ftp_stor_file(
    ftp: FTP,
    remote_dir: str,
    local_path: Path,
    remote_name: str,
    *,
    verify: bool = True,
) -> None:
    expected = local_path.stat().st_size
    ftp_mkdir_p(ftp, remote_dir)
    print(f"[up]   /{remote_dir}/{remote_name} ({expected:,} bytes)")
    with open(local_path, "rb") as fh:
        ftp.storbinary(f"STOR {remote_name}", fh)
    if not verify:
        ftp.cwd("/")
        return
    remote_path = f"{remote_dir}/{remote_name}"
    try:
        actual = ftp.size(remote_name)
    except error_perm as e:
        ftp.cwd("/")
        raise RuntimeError(f"FTP verify failed for /{remote_path}: {e}") from e
    ftp.cwd("/")
    if actual != expected:
        raise RuntimeError(
            f"FTP upload size mismatch for /{remote_path}: "
            f"local={expected:,} remote={actual:,}"
        )


def ftp_stor_root_file(ftp: FTP, local_path: Path, remote_name: str) -> None:
    """Upload a file to site document root (/) with size verification."""
    expected = local_path.stat().st_size
    ftp.cwd("/")
    print(f"[up] /{remote_name} ({expected:,} bytes)")
    with open(local_path, "rb") as fh:
        ftp.storbinary(f"STOR {remote_name}", fh)
    actual = ftp.size(remote_name)
    if actual != expected:
        raise RuntimeError(
            f"FTP upload size mismatch for /{remote_name}: "
            f"local={expected:,} remote={actual:,}"
        )


def deploy_root_crawl_files(ftp: FTP, repo_root: Path) -> int:
    """Upload llms.txt, ai.txt, robots.txt, sitemap.xml and GEO index.html.md."""
    count = 0
    ftp.cwd("/")
    for name in ROOT_CRAWL_FILES:
        local = repo_root / name
        if not local.is_file():
            continue
        print(f"[up] /{name}")
        with open(local, "rb") as fh:
            ftp.storbinary(f"STOR {name}", fh)
        count += 1
    geo_md = repo_root / GEO_SLUG / "index.html.md"
    if geo_md.is_file():
        ftp_stor_file(ftp, GEO_SLUG, geo_md, "index.html.md")
        count += 1
    return count


def deploy_artists_build(ftp: FTP, local_dir: Path) -> int:
    """Publish artist pages from artists_build/*.html → /artists/<slug>/index.html."""
    count = 0
    for html in sorted(local_dir.glob("*.html")):
        remote = f"artists/{html.stem}"
        ftp_stor_file(ftp, remote, html, "index.html")
        count += 1
    return count


def deploy_nested_assets(ftp: FTP, local_dir: Path, remote_prefix: str) -> int:
    """Upload images/CSS in subfolders (e.g. client-portfolio/, hero-premium/, artists/joshua-cole/)."""
    count = 0
    for fpath in sorted(local_dir.rglob("*")):
        if not fpath.is_file() or fpath.name == "code.html":
            continue
        if fpath.suffix.lower() not in SLUG_ASSET_EXT:
            continue
        rel = fpath.relative_to(local_dir)
        if len(rel.parts) < 2:
            continue
        remote_dir = f"{remote_prefix}/{rel.parent.as_posix()}"
        ftp_stor_file(ftp, remote_dir, fpath, fpath.name)
        count += 1
    return count


def ftp_dele_file(ftp: FTP, remote_dir: str, remote_name: str) -> None:
    ftp_mkdir_p(ftp, remote_dir)
    try:
        ftp.delete(remote_name)
    except error_perm:
        pass
    ftp.cwd("/")


def deploy_artists_roster_media(ftp: FTP, artists_dir: Path) -> int:
    """Homepage artist cards use /artists/<slug>/* — upload roster image folders."""
    count = 0
    if not artists_dir.is_dir():
        return 0
    for sub in sorted(artists_dir.iterdir()):
        if not sub.is_dir() or sub.name.startswith("."):
            continue
        remote = f"artists/{sub.name}"
        if sub.name == "katelyn-cole":
            ftp_dele_file(
                ftp,
                remote,
                "katelyn-cole-master-body-piercer-ear-curation-no-duplicates-las-vegas.png",
            )
        for fpath in sorted(sub.iterdir()):
            if not fpath.is_file() or fpath.suffix.lower() not in SLUG_ASSET_EXT:
                continue
            # Bluehost rewrites large portrait PNG to WebP at the same path — deploy webp + jpg only.
            if sub.name == "katelyn-cole" and fpath.suffix.lower() == ".png":
                if "master-body-piercer" in fpath.name:
                    continue
            if sub.name == "katelyn-cole":
                ftp_dele_file(ftp, remote, fpath.name)
            ftp_stor_file(ftp, remote, fpath, fpath.name)
            count += 1
    return count


HTACCESS_MARKER = "# Stitch: prefer static index.html before WordPress\n"
HTACCESS_SNIPPET = HTACCESS_MARKER + """<IfModule mod_dir.c>
DirectoryIndex index.html index.php
</IfModule>

"""


def ftp_mkdir_p(ftp: FTP, remote_path: str) -> None:
    parts = [p for p in remote_path.strip("/").split("/") if p]
    ftp.cwd("/")
    for part in parts:
        try:
            ftp.mkd(part)
        except error_perm:
            pass
        ftp.cwd(part)


def gather_folders() -> dict[str, Path]:
    merged: dict[str, Path] = {}
    for root in SOURCES:
        if not root.is_dir():
            print(f"[error] Source root is not a directory: {root}", file=sys.stderr)
            continue
        for d in sorted(root.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            merged[d.name] = d
    return merged


def ftp_rmtree(ftp: FTP, path: str) -> None:
    ftp.cwd("/")
    try:
        ftp.cwd(path)
    except error_perm:
        return

    for name, meta in ftp.mlsd():
        if name in (".", ".."):
            continue
        if meta.get("type") == "dir":
            ftp_rmtree(ftp, f"{path}/{name}")
            ftp.cwd("/")
            ftp.cwd(path)
        else:
            try:
                ftp.delete(name)
            except error_perm as e:
                print(f"[warn] delete {path}/{name}: {e}")

    ftp.cwd("/")
    try:
        ftp.rmd(path)
    except error_perm as e:
        print(f"[warn] rmd {path}: {e}")


def patch_htaccess(raw: bytes) -> bytes:
    text = raw.decode("utf-8", errors="replace")
    if HTACCESS_MARKER in text:
        return raw
    return (HTACCESS_SNIPPET + text).encode("utf-8")


def main() -> int:
    user = os.environ.get("FTP_USER", "").strip()
    pw = os.environ.get("FTP_PASS", "").strip()
    if not user or not pw:
        print("Set FTP_USER and FTP_PASS in your environment (do not hardcode in this file).", file=sys.stderr)
        return 1

    if not SOURCES[0].is_dir():
        print(
            f"Missing deploy source folder: {SOURCES[0]}\n"
            "Create it or set WOA_DEPLOY_SOURCE to your export root.",
            file=sys.stderr,
        )
        return 1

    merged = gather_folders()
    crawl_written = write_ai_crawl_assets(SOURCES[0])
    if crawl_written:
        print(f"[gen] AI crawl assets: {', '.join(p.name for p in crawl_written)}")

    home_slug = resolve_home_slug(merged)
    home_code_path = merged[home_slug] / "code.html" if home_slug else None
    if home_slug and home_code_path and home_code_path.is_file():
        home_html = home_code_path.read_text(encoding="utf-8", errors="replace")
        if "WOA_BUILD_STAMP:" not in home_html:
            print(
                "[warn] Homepage has no WOA_BUILD_STAMP — run: python3 prepare_site_deploy.py",
                file=sys.stderr,
            )
        if "instagram.com/reel/DDiX988y0tR" not in home_html:
            print(
                "[warn] Homepage missing Joshua interview reel link — run: python3 prepare_site_deploy.py",
                file=sys.stderr,
            )
        if 'id="studio-interview"' not in home_html:
            print(
                "[warn] Homepage missing #studio-interview — run: python3 prepare_site_deploy.py",
                file=sys.stderr,
            )

    if not home_slug:
        home_like = [
            n
            for n in sorted(merged)
            if n.startswith("home") and (merged[n] / "code.html").is_file()
        ]
        print(
            "Could not find a homepage export folder with code.html.\n"
            "Expected something like 'home_work_of_art_tattoo_piercing' or "
            "'home_work_of_art_tattoo' as a direct subfolder of:\n"
            f"  {SOURCES[0]}\n"
            "Fix: put the home export there, or set WOA_HOME_SLUG to the exact folder name.\n"
            f"Folders here (first 40): {sorted(merged.keys())[:40]}",
            file=sys.stderr,
        )
        if home_like:
            print(f"Home-like folders with code.html found: {home_like}", file=sys.stderr)
        return 1

    print(f"SOURCES: {[str(s) for s in SOURCES]}")
    print(f"Unique folders: {len(merged)} (home slug → /index.html: {home_slug})")

    root_media_folder = (
        os.environ.get("WOA_ROOT_MEDIA_FOLDER", "_repo_media").strip() or "_repo_media"
    )

    try:
        ftp = FTP(HOST, timeout=120)
        ftp.login(user, pw)
    except error_perm as e:
        print(
            f"FTP login failed ({e}).\n"
            f"  Host: {HOST}\n"
            f"  User: {user!r}\n"
            "  Use one line: FTP_USER='...' FTP_PASS='...' python3 deploy_stitch_site_root.py\n"
            "  (Do not use the placeholder 'your-password'.)\n"
            "  Reset the FTP password in Bluehost → Advanced → FTP Accounts if needed.",
            file=sys.stderr,
        )
        return 1
    ftp.set_pasv(True)

    try:
        return _deploy_all(ftp, merged, home_slug, root_media_folder)
    except RuntimeError as e:
        print(f"\n[error] {e}", file=sys.stderr)
        try:
            ftp.quit()
        except OSError:
            pass
        return 1


def _deploy_all(
    ftp: FTP,
    merged: dict[str, Path],
    home_slug: str,
    root_media_folder: str,
) -> int:
    buf = BytesIO()
    ftp.retrbinary("RETR .htaccess", buf.write)
    old_ht = buf.getvalue()
    new_ht = patch_htaccess(old_ht)
    if new_ht != old_ht:
        print("[up] /.htaccess (prepend DirectoryIndex for index.html)")
        ftp.cwd("/")
        ftp.storbinary("STOR .htaccess", BytesIO(new_ht))

    uploaded = 0
    uploaded_media_only = 0
    uploaded_artists = 0
    skipped = 0

    n_crawl = deploy_root_crawl_files(ftp, SOURCES[0])
    if n_crawl:
        print(f"[up] {n_crawl} AI crawl file(s) at site root / GEO markdown")

    if "artists_build" in merged:
        n = deploy_artists_build(ftp, merged["artists_build"])
        if n:
            print(f"[up] artists_build → {n} page(s) under /artists/")
            uploaded_artists += n

    artists_root = merged.get("artists")
    if artists_root and artists_root.is_dir():
        n = deploy_artists_roster_media(ftp, artists_root)
        if n:
            print(f"[up] artists roster media → {n} file(s) under /artists/<slug>/")
            uploaded += n

    for slug in sorted(merged.keys()):
        if slug == "artists_build":
            continue
        local_dir = merged[slug]
        code = local_dir / "code.html"

        if code.is_file():
            ftp_mkdir_p(ftp, slug)
            print(f"[up] /{slug}/index.html")
            with open(code, "rb") as fh:
                ftp.storbinary("STOR index.html", fh)

            for fpath in sorted(local_dir.iterdir()):
                if not fpath.is_file() or fpath.name == "code.html":
                    continue
                if fpath.suffix.lower() not in SLUG_ASSET_EXT:
                    continue
                print(f"[up]   asset /{slug}/{fpath.name}")
                with open(fpath, "rb") as bf:
                    ftp.storbinary(f"STOR {fpath.name}", bf)

            n_nested = deploy_nested_assets(ftp, local_dir, slug)
            if n_nested:
                print(f"[up]   nested assets /{slug}/ → {n_nested} file(s)")

            uploaded += 1
            continue

        if slug in SKIP_MEDIA_ONLY_NAMES:
            print(f"[skip] {slug} — excluded from deploy")
            skipped += 1
            continue

        imgs = iter_image_files_direct(local_dir)
        if imgs:
            artist_slug = artist_remote_slug_from_folder(slug)
            if artist_slug:
                remote = f"artists/{artist_slug}"
                for fpath in imgs:
                    ftp_stor_file(ftp, remote, fpath, fpath.name)
                # Pages also reference the Stitch export folder name at site root.
                for fpath in imgs:
                    ftp_stor_file(ftp, slug, fpath, fpath.name)
                uploaded_media_only += 1
                continue
            ftp_mkdir_p(ftp, slug)
            for fpath in imgs:
                print(f"[up]   media /{slug}/{fpath.name}")
                with open(fpath, "rb") as bf:
                    ftp.storbinary(f"STOR {fpath.name}", bf)
            uploaded_media_only += 1
            continue

        print(f"[skip] {slug} — no code.html and no images")
        skipped += 1

    root_imgs = [
        p
        for p in sorted(SOURCES[0].iterdir())
        if p.is_file() and p.suffix.lower() in IMAGE_EXT
    ]
    if root_imgs:
        ftp_mkdir_p(ftp, root_media_folder)
        for fpath in root_imgs:
            print(f"[up]   media /{root_media_folder}/{fpath.name}")
            with open(fpath, "rb") as bf:
                ftp.storbinary(f"STOR {fpath.name}", bf)
        print(f"[up] {len(root_imgs)} loose repo-root image(s) → /{root_media_folder}/")

    home_code = merged[home_slug] / "code.html"
    ftp_stor_root_file(ftp, home_code, "index.html")

    # Force critical assets (common partial-deploy failures).
    artists_dir = merged.get("artists")
    if artists_dir and artists_dir.is_dir():
        n = deploy_artists_roster_media(ftp, artists_dir)
        if n:
            print(f"[up] critical re-push artists media → {n} file(s)")

    print(f"[rm] removing legacy /{LEGACY_PREFIX}/ …")
    ftp_rmtree(ftp, LEGACY_PREFIX)

    ftp.quit()
    home_bytes = home_code.stat().st_size
    print(
        "Done. HTML sections: "
        f"{uploaded}; media-only folders: {uploaded_media_only}; "
        f"artist pages: {uploaded_artists}; skipped: {skipped}. "
        f"Homepage from {home_slug!r} ({home_bytes:,} bytes on server)."
    )
    print("Try: https://workofarttattoo.com/")
    print("View Source → search for WOA_BUILD_STAMP and id=\"studio-interview\"")
    print("Then run: python3 verify_live_deploy.py")
    print(
        "Example slug: "
        "https://workofarttattoo.com/walk_in_tattoos_las_vegas_authority_guide/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
