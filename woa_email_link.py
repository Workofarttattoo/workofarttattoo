"""Public contact link and FormSubmit recipients.

Visible pages use an obfuscated "Email us now" control. The booking recipient
appears in delivered HTML only inside FormSubmit action and ajax URLs.
"""

from __future__ import annotations

import re
from pathlib import Path

FORM_RECIPIENT = "thewhiteknight702@gmail.com"
FORMSUBMIT_ACTION = f"https://formsubmit.co/{FORM_RECIPIENT}"
FORMSUBMIT_AJAX = f"https://formsubmit.co/ajax/{FORM_RECIPIENT}"
EMAIL_US_NOW_LABEL = "Email us now"
EMAIL_US_SCRIPT_SRC = "/woa-email-us.js"

_CHAR_CODES = ",".join(str(ord(ch)) for ch in FORM_RECIPIENT)

EMAIL_US_SCRIPT_JS = f"""(function () {{
  var codes = [{_CHAR_CODES}];
  function address() {{
    var out = "";
    for (var i = 0; i < codes.length; i++) out += String.fromCharCode(codes[i]);
    return out;
  }}
  document.addEventListener("click", function (event) {{
    var node = event.target && event.target.closest ? event.target.closest("[data-woa-email-us]") : null;
    if (!node) return;
    event.preventDefault();
    window.location.href = "mailto:" + address();
  }});
}})();
"""

# Legacy mailboxes that must not remain as visible copy or mailto targets.
_LEGACY_EMAIL = (
    r"booking@workofarttattoo\.com"
    r"|thewhiteknight702@gmail\.com"
    r"|kmorgen14@gmail\.com"
)

FORMSUBMIT_BOOKING_RE = re.compile(
    r"https://formsubmit\.co/(ajax/)?booking@workofarttattoo\.com",
    re.IGNORECASE,
)
FORMSUBMIT_RECIPIENT_RE = re.compile(
    rf"https://formsubmit\.co/(?:ajax/)?{re.escape(FORM_RECIPIENT)}",
    re.IGNORECASE,
)
MAILTO_ANCHOR_RE = re.compile(
    rf"<a\b([^>]*?)\bhref=(['\"])mailto:(?:{_LEGACY_EMAIL})[^'\"]*\2([^>]*)>(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
SCHEMA_EMAIL_WITH_COMMA_RE = re.compile(
    rf'[ \t]*"email"\s*:\s*"(?:{_LEGACY_EMAIL})"\s*,\n',
    re.IGNORECASE,
)
SCHEMA_EMAIL_LAST_RE = re.compile(
    rf',\n[ \t]*"email"\s*:\s*"(?:{_LEGACY_EMAIL})"\s*\n',
    re.IGNORECASE,
)
CLASS_RE = re.compile(r"""\bclass=(['"])(.*?)\1""", re.IGNORECASE | re.DOTALL)
SCRIPT_SPLIT_RE = re.compile(r"(<script\b[^>]*>.*?</script>)", re.IGNORECASE | re.DOTALL)
VISIBLE_EMAIL_RE = re.compile(_LEGACY_EMAIL, re.IGNORECASE)
def email_us_anchor(class_name: str = "") -> str:
    class_attr = f' class="{class_name}"' if class_name else ""
    return f'<a{class_attr} href="#" data-woa-email-us="1">{EMAIL_US_NOW_LABEL}</a>'


def _anchor_from_match(match: re.Match[str]) -> str:
    classes = ""
    for chunk in (match.group(1), match.group(3)):
        found = CLASS_RE.search(chunk or "")
        if found:
            classes = found.group(2)
            break
    return email_us_anchor(classes)


def _protect_formsubmit(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def repl(match: re.Match[str]) -> str:
        saved.append(match.group(0))
        return f"___WOA_FS_{len(saved) - 1}___"

    return FORMSUBMIT_RECIPIENT_RE.sub(repl, text), saved


def _restore_formsubmit(text: str, saved: list[str]) -> str:
    for index, url in enumerate(saved):
        text = text.replace(f"___WOA_FS_{index}___", url)
    return text


def _replace_outside_scripts(text: str) -> str:
    parts = SCRIPT_SPLIT_RE.split(text)
    rebuilt: list[str] = []
    anchor = email_us_anchor()
    for part in parts:
        if part.lower().startswith("<script"):
            rebuilt.append(part)
            continue
        rebuilt.append(VISIBLE_EMAIL_RE.sub(anchor, part))
    return "".join(rebuilt)


def apply_public_email_policy(text: str) -> str:
    """Point FormSubmit at the booking recipient and hide mailbox addresses."""

    def formsubmit_repl(match: re.Match[str]) -> str:
        return FORMSUBMIT_AJAX if match.group(1) else FORMSUBMIT_ACTION

    text = FORMSUBMIT_BOOKING_RE.sub(formsubmit_repl, text)
    text, saved = _protect_formsubmit(text)
    text = SCHEMA_EMAIL_WITH_COMMA_RE.sub("", text)
    text = SCHEMA_EMAIL_LAST_RE.sub("\n", text)
    text = MAILTO_ANCHOR_RE.sub(_anchor_from_match, text)
    text = _replace_outside_scripts(text)
    text = _restore_formsubmit(text, saved)
    if "data-woa-email-us" in text and EMAIL_US_SCRIPT_SRC not in text:
        tag = f'<script defer src="{EMAIL_US_SCRIPT_SRC}"></script>\n'
        idx = text.rfind("</body>")
        if idx != -1:
            text = text[:idx] + tag + text[idx:]
        else:
            text += "\n" + tag
    return text


def write_email_script(root: Path) -> None:
    target = root / "woa-email-us.js"
    if FORM_RECIPIENT in EMAIL_US_SCRIPT_JS:
        raise SystemExit("email script must not contain the mailbox literal")
    target.write_text(EMAIL_US_SCRIPT_JS, encoding="utf-8")
