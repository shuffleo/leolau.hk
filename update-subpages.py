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

Accepted nested entry folder regex (for writings and works):
    ^(?P<pub_date>\d{4}(?:-\d{2}-\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ENTRY_DIR_RE = re.compile(
    r"^(?P<pub_date>\d{4}(?:-\d{2}-\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$"
)

NAV_LINE = (
    "[☁ ABOUT](../)  ||  [⛰ WORKS](../works/)  ||  [⚯ WRITINGS](../writings/)"
)

SECTION_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Leo Lau</title>
    <meta name="description" content="{description}">
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
    <meta name="description" content="{title}">
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


@dataclass
class Entry:
    folder: str
    pub_date: str
    title: str
    path: Path


def title_from_content(content_md: Path, fallback_slug: str) -> str:
    try:
        lines = content_md.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return fallback_slug.replace("-", " ").title()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback_slug.replace("-", " ").title()


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

        pub_date = match.group("pub_date")
        slug = match.group("slug")
        title = title_from_content(content_md, slug)
        entries.append(
            Entry(
                folder=child.name,
                pub_date=pub_date,
                title=title,
                path=child,
            )
        )
    return entries


def write_section_index(section_dir: Path, title: str, description: str) -> None:
    index_html = section_dir / "index.html"
    index_html.write_text(
        SECTION_INDEX_HTML.format(title=title, description=description),
        encoding="utf-8",
    )


def write_entry_index(entry: Entry) -> None:
    entry_index = entry.path / "index.html"
    entry_index.write_text(
        ENTRY_INDEX_HTML.format(title=entry.title),
        encoding="utf-8",
    )


def render_listing_markdown(
    section_title: str,
    section_path: str,
    entries: list[Entry],
    empty_message: str,
) -> str:
    lines = [NAV_LINE, "", "---", "", f"# {section_title}", ""]
    if entries:
        for entry in entries:
            lines.append(
                f"{entry.pub_date} - [{entry.title}](./{entry.folder}/)"
            )
    else:
        lines.append(empty_message)
    lines.append("")
    return "\n".join(lines)


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
    write_section_index(works_dir, "Works", "Media art case studies by Leo Lau")

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
    (works_dir / "content.md").write_text(
        render_listing_markdown(
            section_title="Works",
            section_path="/works",
            entries=works,
            empty_message="No case studies yet.",
        ),
        encoding="utf-8",
    )

    print(
        "Updated subpages:"
        f" writings ({len(writings)}), works ({len(works)})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
