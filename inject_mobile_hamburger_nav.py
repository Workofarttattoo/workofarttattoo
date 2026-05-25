#!/usr/bin/env python3
"""
Inject an accessible mobile hamburger menu on Stitch static HTML exports.

Looks for fixed top navigation (header OR nav.fixed) that contains a
`hidden md:flex` block with in-page/booking links and adds:
- Hamburgers + close icon (mobile only), aria-expanded wiring
- Narrow right-edge panel (not full viewport width) + dim overlay
- Copies of desktop nav anchors (flattened typography)
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from bs4 import BeautifulSoup

_ROOT_A = Path(__file__).resolve().parent
_ROOT_B = Path("/Users/noone/Downloads/stitch_work_of_art_digital_overhaul 2")

SKIP_REL = frozenset(
    (
        "skipped_pages_clipboard.html",
        "joshua.raw.html",
        "katelyn.raw.html",
    )
)


STYLE_BLOCK = """

/* Work of Art — mobile nav (inject_mobile_hamburger_nav.py) — narrow rail + larger type */
html.woa-mnav-lock,
html.woa-mnav-lock body {
  overflow: hidden !important;
  touch-action: none;
}
.woa-mnav-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  z-index: 60;
}
.woa-mnav-panel {
  box-sizing: border-box;
  position: fixed;
  left: auto;
  right: 0;
  top: 0;
  width: 6rem;
  max-width: 96px;
  z-index: 70;
  max-height: min(88vh, 560px);
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  border-left: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom-left-radius: 0.75rem;
  background: rgba(19, 19, 19, 0.98);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: -10px 14px 36px rgba(0, 0, 0, 0.42);
  font-size: 17px;
  line-height: 1.25;
}

.woa-mnav-inner {
  padding: 4.85rem 0.4rem 0.75rem;
}

.woa-mnav-panel a,
.woa-mnav-panel summary {
  word-break: break-word;
  overflow-wrap: anywhere;
  hyphens: auto;
}

.woa-mnav-panel details.mobile-guides-dd > summary {
  list-style: none;
  cursor: pointer;
}
.woa-mnav-panel details.mobile-guides-dd > summary::-webkit-details-marker {
  display: none;
}

.woa-mnav-panel details.mobile-guides-dd .guides-sub {
  padding: 0.25rem 0 0;
  margin: 0;
  border-bottom: 1px solid rgba(68, 71, 72, 0.35);
  padding-bottom: 0.4rem;
  margin-bottom: 0.2rem;
}

"""
MNV_PANEL_CSS_V1 = """.woa-mnav-panel {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  z-index: 70;
  max-height: min(92vh, 640px);
  overflow-y: auto;
  overscroll-behavior: contain;
  border-bottom: 1px solid rgba(68, 71, 72, 0.5);
  background: rgba(19, 19, 19, 0.98);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
}"""

MNV_PANEL_CSS_V2 = """.woa-mnav-panel {
  position: fixed;
  left: auto;
  right: 0;
  top: 0;
  width: min(17.5rem, 78vw);
  max-width: 100%;
  z-index: 70;
  max-height: min(72vh, 480px);
  overflow-y: auto;
  overscroll-behavior: contain;
  border-left: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom-left-radius: 0.75rem;
  background: rgba(19, 19, 19, 0.98);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: -10px 14px 36px rgba(0, 0, 0, 0.42);
}"""

MNV_PANEL_CSS_V3 = """.woa-mnav-panel {
  box-sizing: border-box;
  position: fixed;
  left: auto;
  right: 0;
  top: 0;
  width: 6rem;
  max-width: 96px;
  z-index: 70;
  max-height: min(88vh, 560px);
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  border-left: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom: 1px solid rgba(68, 71, 72, 0.5);
  border-bottom-left-radius: 0.75rem;
  background: rgba(19, 19, 19, 0.98);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: -10px 14px 36px rgba(0, 0, 0, 0.42);
  font-size: 17px;
  line-height: 1.25;
}"""

# Saved-page upgrades (full-bleed v1 → compact panel)
MNV_INNER_CLASSES_OLD = "px-margin-mobile pt-[5.75rem] pb-8"
MNV_INNER_CLASSES_NEW = "woa-mnav-inner"

MNV_LINK_ROW_PY4 = (
    "block py-4 font-nav-link text-nav-link text-on-surface "
    "uppercase tracking-[0.12em] border-b border-outline-variant "
    "hover:text-secondary transition-colors woa-mnav-mobile-link"
)
MOB_LINK_V3_MAIN = (
    "block py-2.5 text-[17px] leading-snug font-semibold text-on-surface "
    "tracking-normal border-b border-outline-variant hover:text-secondary "
    "transition-colors woa-mnav-mobile-link"
)
MOB_LINK_V3_SUB = (
    "block py-1.5 text-[13px] leading-snug font-medium text-secondary pl-3 "
    "border-b border-outline-variant/60 hover:text-secondary hover:bg-surface-container/40 "
    "transition-colors woa-mnav-mobile-link"
)

MNV_LINK_ROW_PY3 = MOB_LINK_V3_MAIN

MNV_TEL_ROW_OLD = (
    "inline-flex items-center gap-3 mt-6 py-4 text-secondary font-label-caps "
    "uppercase tracking-widest"
)
MNV_TEL_ROW_NEW = (
    "inline-flex items-center gap-3 mt-5 py-3 text-secondary font-label-caps "
    "uppercase tracking-widest"
)
MNV_TEL_ROW_V3 = (
    "inline-flex flex-wrap items-center gap-2 mt-4 py-2 text-secondary "
    "text-[13px] leading-tight font-semibold tracking-tight woa-mnav-mobile-link"
)

# Intermediate export (py-3 uppercase, no woa-mnav-mobile-link)
MNV_LINK_ROW_PY3_LEGACY = (
    "block py-3 font-nav-link text-nav-link text-on-surface "
    "uppercase tracking-[0.12em] border-b border-outline-variant "
    "hover:text-secondary transition-colors"
)

SCRIPT_JS = """(function() {
'use strict';
var KEY = '__woaMnavDone';
if (window[KEY]) return;
window[KEY] = true;

function closeAll(openEl) {
  document.querySelectorAll('[data-mobile-nav-toggle][aria-expanded="true"]').forEach(function(btn) {
    if (openEl && btn === openEl) return;
    setOpen(btn, false);
  });
}

function findBits(btn) {
  var pid = btn.getAttribute('aria-controls');
  if (!pid) return null;
  var panel = document.getElementById(pid);
  if (!panel) return null;
  var overlayId = btn.getAttribute('data-overlay-for');
  var overlay = overlayId ? document.getElementById(overlayId) : null;
  return {panel: panel, overlay: overlay};
}

function setOpen(btn, open) {
  var bits = findBits(btn);
  if (!bits) return;
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  btn.setAttribute('aria-label', open ? 'Close menu' : 'Open navigation menu');
  bits.panel.hidden = !open;
  bits.panel.classList.toggle('hidden', !open);
  bits.panel.style.display = open ? 'block' : 'none';
  if (bits.overlay) {
    bits.overlay.hidden = !open;
    bits.overlay.style.display = open ? 'block' : 'none';
    bits.overlay.setAttribute('aria-hidden', open ? 'false' : 'true');
  }
  var openIcon = btn.querySelector('.woa-menu-icon-open');
  var closeIcon = btn.querySelector('.woa-menu-icon-close');
  if (openIcon) openIcon.classList.toggle('hidden', open);
  if (closeIcon) closeIcon.classList.toggle('hidden', !open);
  document.documentElement.classList.toggle('woa-mnav-lock', !!open);
}

document.addEventListener('click', function(e) {
  var inPanel = e.target.closest('.woa-mnav-panel');
  if (inPanel && e.target.closest('details.mobile-guides-dd > summary')) {
    return;
  }
  var mobilink = e.target.closest('.woa-mnav-mobile-link');
  if (mobilink) {
    document.querySelectorAll('[data-mobile-nav-toggle][aria-expanded="true"]').forEach(function(btn2) {
      setOpen(btn2, false);
    });
    return;
  }
  var btn = e.target.closest('[data-mobile-nav-toggle]');
  if (btn && btn.closest('[data-woa-top-shell]')) {
    e.preventDefault();
    var expanded = btn.getAttribute('aria-expanded') === 'true';
    closeAll(btn);
    setOpen(btn, !expanded);
    return;
  }
  var over = e.target.closest('.woa-mnav-overlay');
  if (over) {
    var forBtn = document.querySelector('[data-overlay-for="' + over.id + '"]');
    if (forBtn) setOpen(forBtn, false);
  }
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeAll(null);
});

var mq = window.matchMedia('(min-width: 768px)');
function onWide() {
  if (mq.matches) closeAll(null);
}
if (mq.addEventListener) mq.addEventListener('change', onWide);
else mq.addListener(onWide);
})();\n"""


def collect_files() -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for root in (_ROOT_A, _ROOT_B):
        if not root.is_dir():
            continue
        for p in root.rglob("*.html"):
            if p.name in SKIP_REL:
                continue
            if "artists_raw" in str(p.resolve()):
                continue
            rs = str(p.resolve())
            if rs in seen:
                continue
            seen.add(rs)
            out.append(p)
    return sorted(out, key=lambda p: str(p))


def iter_all_project_html(include_root_b: bool = True) -> list[Path]:
    """Every HTML file under project roots (for CSS/markup patching)."""
    seen: set[str] = set()
    out: list[Path] = []
    roots: list[Path] = [_ROOT_A]
    if include_root_b and _ROOT_B.is_dir():
        roots.append(_ROOT_B)
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*.html"):
            if "__pycache__" in p.parts:
                continue
            rp = str(p.resolve())
            if rp in seen:
                continue
            seen.add(rp)
            out.append(p)
    return sorted(out, key=lambda p: str(p))


def patch_existing_narrow_mnav(include_root_b: bool = True) -> int:
    """
    Update already-deployed injected markup: slim right-edge rail (v3), link rows, tel.
    Safe to run multiple times (files already matching v3 rules are unchanged).
    """
    patched = 0
    for path in iter_all_project_html(include_root_b):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "data-woa-mnav-style" not in raw:
            continue
        new = raw
        if MNV_PANEL_CSS_V1 in new:
            new = new.replace(MNV_PANEL_CSS_V1, MNV_PANEL_CSS_V3)
        if MNV_PANEL_CSS_V2 in new:
            new = new.replace(MNV_PANEL_CSS_V2, MNV_PANEL_CSS_V3)
        if MNV_INNER_CLASSES_OLD in new:
            new = new.replace(MNV_INNER_CLASSES_OLD, MNV_INNER_CLASSES_NEW)
        if MNV_LINK_ROW_PY4 in new:
            new = new.replace(MNV_LINK_ROW_PY4, MOB_LINK_V3_MAIN)
        if MNV_LINK_ROW_PY3_LEGACY in new:
            new = new.replace(MNV_LINK_ROW_PY3_LEGACY, MOB_LINK_V3_MAIN)
        if MNV_TEL_ROW_OLD in new:
            new = new.replace(MNV_TEL_ROW_OLD, MNV_TEL_ROW_V3)
        if MNV_TEL_ROW_NEW in new:
            new = new.replace(MNV_TEL_ROW_NEW, MNV_TEL_ROW_V3)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            patched += 1
    return patched


def cls_join(el) -> str:
    c = el.get("class")
    if not c:
        return ""
    if isinstance(c, str):
        return c
    return " ".join(c)


def pid_for(path: Path) -> str:
    h = hashlib.md5(str(path.resolve()).encode(), usedforsecurity=False).hexdigest()[:10]
    return "w" + h


def find_top_shell(soup: BeautifulSoup):
    for el in soup.find_all("header"):
        cc = cls_join(el)
        if "fixed" in cc and ("top-0" in cc or "sticky" in cc):
            return el
    for el in soup.find_all("nav"):
        cc = cls_join(el)
        if "fixed" in cc and "top-0" in cc:
            return el
    return None


def find_desktop_nav_strip(shell):
    marked = shell.find(attrs={"data-woa-desktop-nav": "1"})
    if marked and marked.name in ("div", "nav"):
        mc = cls_join(marked)
        if "hidden" in mc and "md:flex" in mc:
            return marked
    best = None
    best_key = None  # maximize score, minimize depth

    for el in shell.find_all(["nav", "div"], recursive=True):
        cc = cls_join(el)
        if "hidden" not in cc or "md:flex" not in cc:
            continue
        anchors = []
        for a in el.find_all("a", href=True):
            href = (a.get("href") or "").strip()
            if not href or href.lower().startswith("javascript"):
                continue
            label = a.get_text(strip=True)
            if len(label) < 2:
                continue
            anchors.append(a)
        if len(anchors) < 2:
            continue
        depth = len(list(el.parents))
        score = len(anchors) + (0.35 if el.name == "nav" else 0)
        text_len = sum(len(a.get_text(strip=True)) for a in anchors)
        if text_len < 12 and len(anchors) < 3:
            continue
        key = (score, -text_len, -depth)
        if best_key is None or key > best_key:
            best, best_key = el, key
    return best


def find_book_cta(shell):
    ranked = []
    for c in shell.find_all(["a", "button"]):
        txt = (c.get_text() or "").strip().lower()
        cl = cls_join(c).lower()
        depth = len(list(c.parents))
        score = 0
        if "book" in txt:
            score += 12
        if "appointment" in txt or "consult" in txt:
            score += 6
        if "bg-secondary" in cl:
            score += 5
        if c.name == "button":
            score += 2
        ranked.append((score, -depth, c))
    ranked.sort(key=lambda t: (t[0], t[1]), reverse=True)
    for s, _d, c in ranked:
        if s > 0:
            return c
    if shell.find("button"):
        return shell.find("button")
    return shell.find("a", href=True)


def fill_mobile_navigation(inner: object, soup: BeautifulSoup, nav_strip) -> None:
    """Flatten desktop strip into mobile drawer: top links + Guides accordion."""

    bold_labels = frozenset({"guides"})

    def link_classes(label: str) -> list[str]:
        base = MOB_LINK_V3_MAIN.split()
        if label.strip().lower() in bold_labels:
            base.append("text-secondary")
        return base

    for child in list(nav_strip.children):
        nm = getattr(child, "name", None)
        if not nm:
            continue
        if nm == "a":
            href = (child.get("href") or "").strip()
            label = child.get_text(" ", strip=True).replace("\xa0", " ").strip()
            if not href or len(label) < 2:
                continue
            a = soup.new_tag("a", href=href)
            a["class"] = link_classes(label)
            a.string = label
            inner.append(a)
        elif nm == "details":
            dd = soup.new_tag(
                "details",
                attrs={"class": ["mobile-guides-dd", "border-b", "border-outline-variant", "pb-1"]},
            )
            sm = soup.new_tag(
                "summary",
                attrs={"class": link_classes("Guides")},
            )
            sm.string = "Guides"
            dd.append(sm)
            sub = soup.new_tag("div", attrs={"class": ["guides-sub"]})
            dd.append(sub)
            for la in child.find_all("a", href=True):
                h = (la.get("href") or "").strip()
                lbl = la.get_text(" ", strip=True).replace("\xa0", " ").strip()
                if not h or len(lbl) < 2:
                    continue
                xa = soup.new_tag("a", href=h)
                xa["class"] = MOB_LINK_V3_SUB.split()
                xa.string = lbl[:56] + ("…" if len(lbl) > 56 else "")
                sub.append(xa)
            if not sub.find("a"):
                continue
            inner.append(dd)

def strip_injected_navigation(soup: BeautifulSoup) -> None:
    """Remove prior hamburger markup so the page can be re-injected cleanly."""
    for ov in soup.find_all(attrs={"data-overlay": True}):
        ov.decompose()
    for pn in soup.find_all(attrs={"data-woa-mobile-panel": True}):
        pn.decompose()
    for btn in soup.find_all(attrs={"data-mobile-nav-toggle": True}):
        btn.decompose()
    for st in soup.find_all("style", attrs={"data-woa-mnav-style": True}):
        st.decompose()
    for sc in soup.find_all("script", attrs={"data-woa-mnav-script": True}):
        sc.decompose()
    for sh in soup.find_all(attrs={"data-woa-top-shell": True}):
        for att in ("data-woa-top-shell", "data-woa-mnav-done"):
            if att in sh.attrs:
                del sh[att]


def ensure_style(head, soup: BeautifulSoup):
    needle = "woa-mnav-overlay"
    for st in head.find_all("style"):
        if st.string and needle in st.string:
            return
    tag = soup.new_tag("style", attrs={"data-woa-mnav-style": "1"})
    tag.string = STYLE_BLOCK
    head.append(tag)


def ensure_script_before_body_close(soup: BeautifulSoup, replace: bool = False):
    body = soup.find("body")
    if not body:
        return
    old = body.find(attrs={"data-woa-mnav-script": True})
    if old and replace:
        old.decompose()
    if body.find(attrs={"data-woa-mnav-script": True}):
        return
    sc = soup.new_tag(
        "script",
        attrs={"type": "text/javascript", "data-woa-mnav-script": "1"},
    )
    sc.string = SCRIPT_JS
    body.append(sc)


def build_toggle_btn(soup, pid: str, overlay_id: str):
    panel_id = pid + "_panel"
    btn = soup.new_tag(
        "button",
        attrs={
            "type": "button",
            "class": ["md:!hidden", "inline-flex", "items-center", "justify-center",
                      "rounded-sm", "p-3", "-mr-2", "text-on-surface-variant",
                      "hover:text-secondary", "transition-colors", "focus:outline-none",
                      "focus-visible:ring-2", "focus-visible:ring-secondary", "focus-visible:ring-offset-2",
                      "focus-visible:ring-offset-background", "shrink-0", "touch-manipulation"],
            "aria-expanded": "false",
            "aria-controls": panel_id,
            "data-mobile-nav-toggle": "1",
            "data-overlay-for": overlay_id,
            "aria-label": "Open navigation menu",
        },
    )
    open_ic = soup.new_tag(
        "span",
        attrs={
            "class": ["material-symbols-outlined", "text-3xl", "woa-menu-icon-open", "leading-none"],
            "aria-hidden": "true",
        },
    )
    open_ic.string = "menu"
    close_ic = soup.new_tag(
        "span",
        attrs={
            "class": ["material-symbols-outlined", "text-3xl", "woa-menu-icon-close", "hidden", "leading-none"],
            "aria-hidden": "true",
        },
    )
    close_ic.string = "close"
    btn.append(open_ic)
    btn.append(close_ic)
    return btn, panel_id


def rel_display(p: Path) -> str:
    try:
        return str(p.relative_to(_ROOT_A))
    except ValueError:
        try:
            return str(p.relative_to(_ROOT_B))
        except ValueError:
            return str(p)


def inject_for_file(path: Path, force: bool = False) -> tuple[bool, str]:
    """
    Returns (wrote_file, status).
    status is one of: ok, already_injected, no_top_shell, no_nav_strip, too_few_anchors, no_cta
    """
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    shell = find_top_shell(soup)
    if not shell:
        print(f"[skip] {rel_display(path)}: no fixed top header/nav matched")
        return False, "no_top_shell"

    pid = pid_for(path)
    overlay_id = pid + "_ov"

    done = shell.get("data-woa-mnav-done")
    if done and not force:
        return False, "already_injected"
    if done and force:
        strip_injected_navigation(soup)
        shell = find_top_shell(soup)
        if not shell:
            return False, "no_top_shell"

    nav_strip = find_desktop_nav_strip(shell)
    if not nav_strip:
        msg = f"[skip] {path.name}: no desktop nav strip matched"
        print(msg)
        return False, "no_nav_strip"

    n_anchors = len(nav_strip.find_all("a", href=True))
    if n_anchors < 2:
        msg = f"[skip] {path.name}: too few usable links ({n_anchors})"
        print(msg)
        return False, "too_few_anchors"

    book = find_book_cta(shell)
    if not book:
        msg = f"[skip] {path.name}: no booking CTA found"
        print(msg)
        return False, "no_cta"

    head = soup.find("head")
    if head:
        existing_mnav = soup.find(attrs={"data-woa-mnav-style": True})
        if existing_mnav and force:
            existing_mnav.decompose()
        ensure_style(head, soup)

    for rogue in shell.find_all(attrs={"data-mobile-nav-toggle": True}):
        rogue.decompose()

    btn, panel_id = build_toggle_btn(soup, pid, overlay_id)

    book.insert_before(btn)

    tel_href = None
    tel_label = None
    for a in shell.find_all("a", href=True):
        h = (a.get("href") or "").strip()
        if h.startswith("tel:"):
            tel_href = h
            tel_label = a.get_text(" ", strip=True) or "Call studio"
            break

    panel = soup.new_tag(
        "div",
        attrs={
            "id": panel_id,
            "class": ["woa-mnav-panel", "md:hidden", "hidden"],
            "role": "navigation",
            "aria-label": "Primary",
            "hidden": "",
            "style": "display:none",
            "data-woa-mobile-panel": "1",
        },
    )
    inner = soup.new_tag("div", attrs={"class": ["woa-mnav-inner"]})
    fill_mobile_navigation(inner, soup, nav_strip)

    if tel_href:
        tel = soup.new_tag(
            "a",
            href=tel_href,
            attrs={"class": ["inline-flex", "flex-wrap", "items-center", "gap-2", "mt-4",
                              "py-2", "text-secondary", "text-[13px]", "leading-tight",
                              "font-semibold", "tracking-tight", "woa-mnav-mobile-link"]},
        )
        tel.append(soup.new_tag("span", attrs={"class": ["material-symbols-outlined"], "aria-hidden": "true"}))
        tel.find("span").string = "call"
        lbl = soup.new_tag("span")
        lbl.string = tel_label
        tel.append(lbl)
        inner.append(tel)

    panel.append(inner)

    overlay = soup.new_tag(
        "div",
        attrs={
            "id": overlay_id,
            "class": ["woa-mnav-overlay", "md:!hidden", "hidden"],
            "hidden": "",
            "style": "display:none",
            "aria-hidden": "true",
            "data-overlay": "1",
        },
    )

    shell.insert_after(overlay)
    overlay.insert_after(panel)

    shell["data-woa-top-shell"] = "1"
    shell["data-woa-mnav-done"] = "1"

    ensure_script_before_body_close(soup, replace=bool(force))
    path.write_text(str(soup), encoding="utf-8")
    return True, "ok"


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print per-file status (including already-injected files)",
    )
    ap.add_argument(
        "--patch-narrow-panel",
        action="store_true",
        help="Rewrite CSS/markup on pages that already have injected mobile nav "
        "(narrow right drawer, shorter menu); then exit.",
    )
    ap.add_argument(
        "--no-root-b",
        action="store_true",
        help=f"Exclude second project root ({_ROOT_B.name}) from scan/patch.",
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="Print scan set paths and exit (no injection).",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Re-inject even if data-woa-mnav-done is present (rebuild panel/CSS/JS).",
    )
    args = ap.parse_args()

    if args.patch_narrow_panel:
        n_patched = patch_existing_narrow_mnav(include_root_b=not args.no_root_b)
        print(f"Patched narrower mobile menu in {n_patched} HTML file(s).")
        return 0

    files = collect_files()
    if args.list:
        for p in files:
            print(rel_display(p))
        print(f"\n{len(files)} file(s) in scan set.")
        return 0

    n_ok = 0
    skips: dict[str, int] = {}
    for p in files:
        try:
            did, status = inject_for_file(p, force=bool(args.force))
            if did:
                print(f"[ok] {rel_display(p)}")
                n_ok += 1
            else:
                skips[status] = skips.get(status, 0) + 1
                if args.verbose and status == "already_injected":
                    print(f"[—] {rel_display(p)}: already has mobile nav")
        except Exception as e:
            print(f"[err] {p}: {e}", file=sys.stderr)
            return 1

    print(f"\nEnhanced {n_ok} file(s).")
    if n_already := skips.pop("already_injected", 0):
        print(
            f"Skipped {n_already} file(s) that already include mobile nav "
            '("data-woa-mnav-done"). Re-run is a no-op for those.'
        )
    for k, c in sorted(skips.items()):
        print(f"  ({k}: {c} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
