#!/usr/bin/env python3
"""
translate_npd_pass.py — translate npd-pass.com/index.html into French (fr/index.html).

Reuses the Kimi K2.6 translation pipeline + glossary from
../passpharmacy.ca/translate_to_french.py.

Result:
  fr/index.html   — French version with self-referential canonical
  index.html      — English page gets hreflang en-CA ↔ fr-CA cross-links added

Run:
  cd "Websites 🌏/npd-pass.com code"
  export KIMI_API_KEY="sk-..."
  python3 translate_npd_pass.py
"""

from __future__ import annotations
import os, sys
from pathlib import Path

# Reuse the translator helpers from the passpharmacy.ca pipeline
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "passpharmacy.ca"))
from translate_to_french import (   # noqa: E402
    collect_translatable_strings, batch_translate,
)
from bs4 import BeautifulSoup       # noqa: E402

SITE_ROOT = "https://npd-pass.com"
EN_FILE = HERE / "index.html"
FR_DIR = HERE / "fr"
FR_FILE = FR_DIR / "index.html"


def update_canonical_and_hreflang_fr(soup: BeautifulSoup) -> None:
    fr_url = f"{SITE_ROOT}/fr/"
    en_url = f"{SITE_ROOT}/"
    # Canonical
    canon = soup.find("link", rel="canonical")
    if canon:
        canon["href"] = fr_url
    elif soup.head:
        soup.head.append(soup.new_tag("link", rel="canonical", href=fr_url))
    # og:url
    og_url = soup.find("meta", property="og:url")
    if og_url:
        og_url["content"] = fr_url
    # Strip old hreflang
    for hl in soup.find_all("link", rel="alternate"):
        if hl.get("hreflang"):
            hl.decompose()
    # New hreflang
    if soup.head:
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="en-CA", href=en_url))
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="fr-CA", href=fr_url))
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=en_url))
    # <html lang> + og:locale
    if soup.html:
        soup.html["lang"] = "fr-CA"
    og_locale = soup.find("meta", property="og:locale")
    if og_locale:
        og_locale["content"] = "fr_CA"
    elif soup.head:
        soup.head.append(soup.new_tag("meta", attrs={"property": "og:locale", "content": "fr_CA"}))


def update_english_hreflang(en_path: Path) -> None:
    """Add hreflang to the English page pointing at fr/"""
    txt = en_path.read_text()
    soup = BeautifulSoup(txt, "html.parser")
    en_url = f"{SITE_ROOT}/"
    fr_url = f"{SITE_ROOT}/fr/"
    # Strip existing hreflang first
    for hl in soup.find_all("link", rel="alternate"):
        if hl.get("hreflang"):
            hl.decompose()
    if soup.head:
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="en-CA", href=en_url))
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="fr-CA", href=fr_url))
        soup.head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=en_url))
    en_path.write_text(str(soup))


def fix_asset_paths(soup: BeautifulSoup) -> None:
    """Pages move from / to /fr/ — relative asset paths need to climb a level."""
    for tag_name, attr in [("link", "href"), ("script", "src"), ("img", "src")]:
        for el in soup.find_all(tag_name):
            v = el.get(attr)
            if not v:
                continue
            if v.startswith(("#", "data:", "http://", "https://", "//", "/", "../")):
                continue
            el[attr] = "../" + v


def main() -> None:
    if not os.environ.get("KIMI_API_KEY"):
        print("ERROR: set KIMI_API_KEY first.", file=sys.stderr)
        sys.exit(1)
    if not EN_FILE.exists():
        print(f"ERROR: {EN_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    if FR_FILE.exists():
        print(f"{FR_FILE.relative_to(HERE)} already exists — delete it first to re-translate.")
        sys.exit(0)
    FR_DIR.mkdir(exist_ok=True)

    print(f"→ {EN_FILE.relative_to(HERE)}")
    soup = BeautifulSoup(EN_FILE.read_text(), "html.parser")
    jobs = collect_translatable_strings(soup)
    print(f"  {len(jobs)} translatable strings")
    batch_translate(jobs, batch_size=25)

    fix_asset_paths(soup)
    update_canonical_and_hreflang_fr(soup)

    FR_FILE.write_text(str(soup))
    print(f"  wrote {FR_FILE.relative_to(HERE)}")

    update_english_hreflang(EN_FILE)
    print(f"  added hreflang to {EN_FILE.relative_to(HERE)}")


if __name__ == "__main__":
    main()
