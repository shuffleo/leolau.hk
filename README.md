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
- Run `python3 update-subpages.py` to regenerate section index files, refresh listing pages, and update `articles.json`.

## URL System

Article URLs use a Notion-style scheme: `{title-slug}-{32-char-hex-id}`.

- **Folder name** is `{initial-title-slug}-{id}` — created once, never renamed.
- **Browser URL** auto-updates to `{current-title-slug}-{id}` via `history.replaceState` after the page loads.
- **Stale URLs** (with outdated title slugs) still resolve: a root `404.html` extracts the hex ID, looks up `articles.json`, and redirects to the canonical folder.

### Adding a new article

1. Generate a 32-char hex ID: `openssl rand -hex 16`
2. Create a folder: `writings/{title-slug}-{id}/`
3. Add `content.md` inside it (include a `# Title` heading and `Published: YYYY-MM-DD`).
4. Run `python3 update-subpages.py` — this regenerates `index.html`, the listings page, and `articles.json`.

### Adding a new work

1. Generate a 32-char hex ID: `openssl rand -hex 16`
2. Create a folder: `works/{title-slug}-{id}/`
3. Add `content.md` inside it (with `# Title`, `Year:`, `Type:`, and a YouTube link).
4. Add a `preview.webp` image (used for hover preview on the works table).
5. Manually add a row to `works/content.md` (custom table layout).
6. Run `python3 update-subpages.py` — this regenerates `index.html` and `articles.json`.

### Changing an article title

Edit the `# Title` heading in `content.md`. That's it. No folder renames or link updates needed — `replaceState` handles the URL, and `update-subpages.py` picks up the new title for the listing page.

## Images

- All images should be in **WebP** format for optimal loading speed.
- Every `.webp` image has a tiny `*-tiny.webp` sibling (~32px wide, <500 bytes) used as a blur placeholder.
- Run `python3 optimize-images.py` for a dry-run preview of convertible images.
- Run `python3 optimize-images.py --run` to convert all JPG/JPEG/PNG to WebP, delete the originals, and generate any missing blur thumbnails.
- After conversion, update any markdown references from `.jpg`/`.png` to `.webp`.

## Blur-Up Image Loading

All `.webp` images in articles use a Medium-style blur-up loading effect:

1. A tiny blurred placeholder (`*-tiny.webp`) loads instantly.
2. The full image loads in the background.
3. When ready, the full image fades in over the blur, then the blur hides.

This applies to both inline article images and the works table hover previews. The effect degrades gracefully — if no tiny version exists, the image loads normally.

## Works Hover Preview

- Links in the works table that point to folders with a 32-char hex ID automatically get a hover preview.
- The preview image is loaded from `preview.webp` inside the work's folder (with `preview-tiny.webp` as the blur placeholder).
- On desktop, hovering a title shows the image large and tilted behind the text. Disabled on touch devices.

## Acknowledgments

This project uses the following open-source libraries:

- **[Marked.js](https://github.com/markedjs/marked)** - A markdown parser and compiler. Built for speed. Licensed under [MIT](https://github.com/markedjs/marked/blob/master/LICENSE).
- **[marked-extended-tables](https://github.com/calculuschild/marked-extended-tables)** - Extends Markdown tables with column spanning, row spanning, and multi-row headers.
- **[jsDelivr](https://www.jsdelivr.com/)** - A free, fast, and reliable CDN for open-source projects. Used to serve the Marked.js library.

This site was vibecoded with [Cursor](https://cursor.sh/).