#!/usr/bin/env python3
"""
Maintain writings pages and the writings homepage listing.

Exact filename conventions:
1) Writings homepage files (must exist at repo root under writings/):
   - writings/index.html
   - writings/content.md
2) Article pages (one directory per article under writings/):
   - writings/<article-folder>/index.html
   - writings/<article-folder>/content.md

Exact accepted article folder-name regex:
    ^(?P<pub_date>\\d{4}(?:-\\d{2}-\\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$

Examples:
    2015-learning-to-think
    2025-03-13-human-ai-collaboration

Exact markdown output template for writings/content.md:
    # Writings

    YYYY[-MM-DD] - [Article Title](/writings/<article-folder>/)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ARTICLE_DIR_RE = re.compile(
    r"^(?P<pub_date>\d{4}(?:-\d{2}-\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$"
)

WRITINGS_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Writings - Leo Lau</title>
    <meta name="description" content="Writings by Leo Lau">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="stylesheet" href="/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <div class="container">
        <div id="content" class="markdown-content">
            <div class="loading">Loading content...</div>
        </div>
    </div>

    <script src="/app.js"></script>
</body>
</html>
"""

ARTICLE_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Leo Lau</title>
    <meta name="description" content="{title}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="stylesheet" href="/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
    <div class="container">
        <div id="content" class="markdown-content">
            <div class="loading">Loading content...</div>
        </div>
    </div>

    <script src="/app.js"></script>
</body>
</html>
"""


@dataclass
class Article:
    folder: str
    pub_date: str
    title: str
    path: Path


def title_from_content(content_md: Path, slug: str) -> str:
    try:
        lines = content_md.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return slug.replace("-", " ").title()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return slug.replace("-", " ").title()


def discover_articles(writings_dir: Path) -> list[Article]:
    articles: list[Article] = []
    if not writings_dir.exists():
        return articles

    for child in writings_dir.iterdir():
        if not child.is_dir():
            continue
        match = ARTICLE_DIR_RE.match(child.name)
        if not match:
            continue
        content_md = child / "content.md"
        if not content_md.exists():
            continue
        pub_date = match.group("pub_date")
        slug = match.group("slug")
        title = title_from_content(content_md, slug)
        articles.append(
            Article(
                folder=child.name,
                pub_date=pub_date,
                title=title,
                path=child,
            )
        )
    return articles


def write_writings_index(writings_dir: Path) -> None:
    index_html = writings_dir / "index.html"
    index_html.write_text(WRITINGS_INDEX_HTML, encoding="utf-8")


def write_article_index(article: Article) -> None:
    article_index = article.path / "index.html"
    article_index.write_text(
        ARTICLE_INDEX_HTML.format(title=article.title),
        encoding="utf-8",
    )


def render_writings_markdown(articles: list[Article]) -> str:
    lines = ["# Writings", ""]
    for article in articles:
        lines.append(
            f"{article.pub_date} - [{article.title}](/writings/{article.folder}/)"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    writings_dir = repo_root / "writings"
    writings_dir.mkdir(parents=True, exist_ok=True)

    articles = discover_articles(writings_dir)
    articles.sort(key=lambda a: (a.pub_date, a.folder), reverse=True)

    write_writings_index(writings_dir)
    for article in articles:
        write_article_index(article)

    writings_content = writings_dir / "content.md"
    writings_content.write_text(render_writings_markdown(articles), encoding="utf-8")

    print(f"Updated writings homepage with {len(articles)} article(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
