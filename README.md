# Personal Site

This is the repository for my personal website.

**Visit the live site: [leolau.hk](https://leolau.hk)**

This is a clean, Notion-style markdown reader built as a multi-page application. The site automatically loads and renders markdown content.

## Advanced Tables

- Advanced table features (column span, row span, multi-row headers) are enabled via `marked-extended-tables`.
- Dependency install command: `npm install marked-extended-tables`
- The extension script is loaded in page templates and applied in `app.js` before markdown rendering.

## Subpages

- The top navigation links to `ABOUT` (`/`), `WORKS` (`/works/`), and `WRITINGS` (`/writings/`).
- `writings/` and `works/` are list-style sections with nested entry pages at `<section>/<folder>/index.html`, each paired with `<section>/<folder>/content.md`.
- Nested entry folders for `writings/` and `works/` follow `YYYY[-MM-DD]-slug` (regex: `^(?P<pub_date>\d{4}(?:-\d{2}-\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$`).
- Run `python3 update-subpages.py` to regenerate section index files and refresh `writings/content.md` and `works/content.md`.

## Acknowledgments

This project uses the following open-source libraries:

- **[Marked.js](https://github.com/markedjs/marked)** - A markdown parser and compiler. Built for speed. Licensed under [MIT](https://github.com/markedjs/marked/blob/master/LICENSE).
- **[marked-extended-tables](https://github.com/calculuschild/marked-extended-tables)** - Extends Markdown tables with column spanning, row spanning, and multi-row headers.
- **[jsDelivr](https://www.jsdelivr.com/)** - A free, fast, and reliable CDN for open-source projects. Used to serve the Marked.js library.

This site was vibecoded with [Cursor](https://cursor.sh/).