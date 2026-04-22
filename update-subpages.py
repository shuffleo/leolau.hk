#!/usr/bin/env python3
r"""
Maintain section subpages for writings and works.

This script keeps:
1) Section homepages:
   - writings/index.html + writings/content.md
   - works/index.html + works/content.md
2) Nested entries for writings and works:
   - <section>/<entry-folder>/index.html
   - <section>/<entry-folder>/content.md
3) Article registry:
   - writings/articles.json  (and works/articles.json when entries exist)

Accepted nested entry folder format:
    {title-slug}-{32-char-hex-id}
    e.g. my-article-title-3199786d637a80d0bf78e442c18613df

Folder regex:
    ^(?P<slug>.+)-(?P<id>[0-9a-f]{32})$
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape as _esc
from pathlib import Path
from xml.sax.saxutils import escape as _xml_esc
import json
import re


ENTRY_DIR_RE = re.compile(
    r"^(?P<slug>.+)-(?P<id>[0-9a-f]{32})$"
)

NAV_LINE = (
    "[ABOUT](../)  ||  [WORKS](../works/)  ||  [WRITINGS](../writings/)"
)

SITE_URL = "https://leolau.hk"
IMAGE_MD_RE = re.compile(r"!\[.*?\]\(\./([^)]+\.webp)\)")
STRIP_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
STRIP_MD_FMT_RE = re.compile(r"[*_`~]+")

SECTION_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Leo Lau</title>
    <meta name="description" content="{description}">
{og_tags}
    <link rel="alternate" type="application/rss+xml" title="Leo Lau" href="/feed.xml">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="stylesheet" href="../styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked-extended-tables/lib/index.umd.js"></script>
</head>
<body>
    <div class="container">
        <div id="content" class="markdown-content">
            <div class="loading">Loading content...</div>
        </div>
    </div>

    <script src="../app.js"></script>
</body>
</html>
"""

ENTRY_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Leo Lau</title>
    <meta name="description" content="{description}">
{og_tags}
    <link rel="alternate" type="application/rss+xml" title="Leo Lau" href="/feed.xml">
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link rel="stylesheet" href="../../styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked-extended-tables/lib/index.umd.js"></script>
</head>
<body>
    <div class="container">
        <div id="content" class="markdown-content">
            <div class="loading">Loading content...</div>
        </div>
    </div>

    <script src="../../app.js"></script>
</body>
</html>
"""


PUB_DATE_RE = re.compile(r"^Published:\s*(\d{4}(?:-\d{2}-\d{2})?)", re.IGNORECASE)


@dataclass
class Entry:
    folder: str
    entry_id: str
    pub_date: str
    title: str
    path: Path


def _parse_content(content_md: Path, fallback_slug: str) -> tuple[str, str]:
    """Return (title, pub_date) extracted from a content.md file."""
    title = fallback_slug.replace("-", " ").title()
    pub_date = ""
    try:
        lines = content_md.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return title, pub_date

    for line in lines:
        stripped = line.strip()
        if not title or title == fallback_slug.replace("-", " ").title():
            if stripped.startswith("# "):
                title = stripped[2:].strip()
        date_match = PUB_DATE_RE.match(stripped)
        if date_match:
            pub_date = date_match.group(1)
    return title, pub_date


DESC_RE = re.compile(r"^Description:\s*(.+)", re.IGNORECASE)


def _extract_description(content_md: Path, max_length: int = 155) -> str:
    """Return explicit Description: metadata if present, otherwise first body paragraph."""
    try:
        lines = content_md.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return ""

    past_separator = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not past_separator:
                past_separator = True
                continue
            break
        if not past_separator:
            m = DESC_RE.match(stripped)
            if m:
                return m.group(1).strip()

    past_separator = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            past_separator = True
            continue
        if not past_separator:
            continue
        if not stripped or stripped.startswith(("!", ">", "#", "[ABOUT]", "|")):
            continue
        text = STRIP_MD_LINK_RE.sub(r"\1", stripped)
        text = STRIP_MD_FMT_RE.sub("", text)
        if len(text) > max_length:
            text = text[:max_length].rsplit(" ", 1)[0] + "\u2026"
        return text
    return ""


def _extract_first_image(content_md: Path, entry_path: Path) -> str | None:
    """Return the filename of the first .webp image, or preview.webp as fallback."""
    try:
        text = content_md.read_text(encoding="utf-8")
    except FileNotFoundError:
        text = ""

    match = IMAGE_MD_RE.search(text)
    if match:
        return match.group(1)
    if (entry_path / "preview.webp").exists():
        return "preview.webp"
    return None


def _build_og_tags(
    title: str, description: str, url: str, image_url: str | None = None,
) -> str:
    """Return indented OG and Twitter meta tags."""
    e = lambda s: _esc(s, quote=True)
    lines = [
        f'    <meta property="og:title" content="{e(title)}">',
        f'    <meta property="og:description" content="{e(description)}">',
        f'    <meta property="og:url" content="{e(url)}">',
    ]
    if image_url:
        lines.append(f'    <meta property="og:image" content="{e(image_url)}">')
        lines.append('    <meta name="twitter:card" content="summary_large_image">')
    else:
        lines.append('    <meta name="twitter:card" content="summary">')
    return "\n".join(lines)


def discover_entries(section_dir: Path) -> list[Entry]:
    entries: list[Entry] = []
    if not section_dir.exists():
        return entries

    for child in section_dir.iterdir():
        if not child.is_dir():
            continue
        match = ENTRY_DIR_RE.match(child.name)
        if not match:
            continue

        content_md = child / "content.md"
        if not content_md.exists():
            continue

        slug = match.group("slug")
        entry_id = match.group("id")
        title, pub_date = _parse_content(content_md, slug)
        entries.append(
            Entry(
                folder=child.name,
                entry_id=entry_id,
                pub_date=pub_date,
                title=title,
                path=child,
            )
        )
    return entries


def write_section_index(section_dir: Path, title: str, description: str) -> None:
    section = section_dir.name
    url = f"{SITE_URL}/{section}/"
    og_tags = _build_og_tags(title, description, url)
    index_html = section_dir / "index.html"
    index_html.write_text(
        SECTION_INDEX_HTML.format(
            title=_esc(title),
            description=_esc(description, quote=True),
            og_tags=og_tags,
        ),
        encoding="utf-8",
    )


def write_entry_index(entry: Entry) -> None:
    content_md = entry.path / "content.md"
    section = entry.path.parent.name
    desc = _extract_description(content_md) or entry.title
    image_file = _extract_first_image(content_md, entry.path)

    canonical_url = f"{SITE_URL}/{section}/{entry.folder}/"
    image_url = f"{canonical_url}{image_file}" if image_file else None
    og_tags = _build_og_tags(entry.title, desc, canonical_url, image_url)

    entry_index = entry.path / "index.html"
    entry_index.write_text(
        ENTRY_INDEX_HTML.format(
            title=_esc(entry.title),
            description=_esc(desc, quote=True),
            og_tags=og_tags,
        ),
        encoding="utf-8",
    )


def render_listing_markdown(
    section_title: str,
    section_path: str,
    entries: list[Entry],
    empty_message: str,
) -> str:
    lines = [NAV_LINE, "", f"### {section_title}", ""]
    if entries:
        for entry in entries:
            lines.append(
                f"{entry.pub_date} - [{entry.title}](./{entry.folder}/)"
            )
    else:
        lines.append(empty_message)
    lines.append("")
    return "\n".join(lines)


def write_articles_json(section_dir: Path, entries: list[Entry]) -> None:
    registry = {e.entry_id: e.folder for e in entries}
    (section_dir / "articles.json").write_text(
        json.dumps(registry, indent=2) + "\n",
        encoding="utf-8",
    )


def _rfc822(date_str: str) -> str:
    """Convert YYYY-MM-DD or YYYY to RFC 822 date string."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y")
        except ValueError:
            return ""
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def write_rss_feed(repo_root: Path, entries: list[Entry]) -> None:
    """Write an RSS 2.0 feed.xml at the repo root."""
    items: list[str] = []
    for entry in entries:
        section = entry.path.parent.name
        link = f"{SITE_URL}/{section}/{entry.folder}/"
        content_md = entry.path / "content.md"
        desc = _xml_esc(_extract_description(content_md) or entry.title)
        pub_date = _rfc822(entry.pub_date)
        pub_line = f"\n      <pubDate>{pub_date}</pubDate>" if pub_date else ""
        items.append(
            f"    <item>\n"
            f"      <title>{_xml_esc(entry.title)}</title>\n"
            f"      <link>{_xml_esc(link)}</link>\n"
            f"      <guid>{_xml_esc(link)}</guid>\n"
            f"      <description>{desc}</description>{pub_line}\n"
            f"    </item>"
        )

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Leo Lau</title>\n"
        f"    <link>{SITE_URL}/</link>\n"
        "    <description>Art, writings, and projects by Leo Lau</description>\n"
        "    <language>en</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f'    <atom:link href="{SITE_URL}/feed.xml" rel="self" '
        f'type="application/rss+xml"/>\n'
        + "\n".join(items) + "\n"
        "  </channel>\n"
        "</rss>\n"
    )
    (repo_root / "feed.xml").write_text(feed, encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parent

    writings_dir = repo_root / "writings"
    works_dir = repo_root / "works"

    writings_dir.mkdir(parents=True, exist_ok=True)
    works_dir.mkdir(parents=True, exist_ok=True)

    writings = discover_entries(writings_dir)
    works = discover_entries(works_dir)
    writings.sort(key=lambda e: (e.pub_date, e.folder), reverse=True)
    works.sort(key=lambda e: (e.pub_date, e.folder), reverse=True)

    write_section_index(writings_dir, "Writings", "Writings by Leo Lau")
    write_section_index(works_dir, "Works", "Art and projects by Leo Lau")

    for entry in writings:
        write_entry_index(entry)
    for entry in works:
        write_entry_index(entry)

    (writings_dir / "content.md").write_text(
        render_listing_markdown(
            section_title="Writings",
            section_path="/writings",
            entries=writings,
            empty_message="No writings yet.",
        ),
        encoding="utf-8",
    )
    # works/content.md uses a custom table layout; only generate if missing
    works_content = works_dir / "content.md"
    if not works_content.exists():
        works_content.write_text(
            render_listing_markdown(
                section_title="Works",
                section_path="/works",
                entries=works,
                empty_message="No case studies yet.",
            ),
            encoding="utf-8",
        )

    write_articles_json(writings_dir, writings)
    if works:
        write_articles_json(works_dir, works)

    all_entries = sorted(writings + works, key=lambda e: (e.pub_date, e.folder), reverse=True)
    write_rss_feed(repo_root, all_entries)

    print(
        "Updated subpages:"
        f" writings ({len(writings)}), works ({len(works)})."
        f" RSS feed: {len(all_entries)} item(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
