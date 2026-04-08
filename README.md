# Personal Site

This is the repository for my personal website.

**Visit the live site: [leolau.hk](https://leolau.hk)**

This is a clean, Notion-style markdown reader built as a multi-page static site hosted on GitHub Pages. There is no build step — every page is plain HTML that loads and renders Markdown client-side via Marked.js.

## Tech Stack

- Static HTML/CSS/JS, hosted on **GitHub Pages**
- **Marked.js** (loaded from jsDelivr CDN) for client-side Markdown rendering
- **marked-extended-tables** for column span, row span, and multi-row header support (declared in `package.json`)
- Shared `app.js` and `styles.css` at the repo root, referenced by all pages

## Site Structure


| Path         | Role                                                                       |
| ------------ | -------------------------------------------------------------------------- |
| `/`          | Homepage (`index.html` + `content.md`)                                     |
| `/writings/` | Listing page + individual essay subpages                                   |
| `/works/`    | Listing page (custom table with hover previews) + individual work subpages |


Top navigation links — **ABOUT** (`/`), **WORKS** (`/works/`), **WRITINGS** (`/writings/`) — appear in every `content.md`. The current section is highlighted with a 🕶️ emoji by `app.js`.

## Content Markdown Structure

Every `content.md` starts with a nav line:

```
[ABOUT](../../)  ||  [WORKS](../../works/)  ||  [WRITINGS](../../writings/)
```

### Writings

```
# Title of the Essay

Published: YYYY-MM-DD
Author: Name

---

[body text, images, links]
```

- `# Title` is the source of truth for the URL slug and listing.
- `Published:` and `Author:` are metadata lines immediately after the title, each ending with two trailing spaces for a Markdown line break.

### Works

```
# Title of the Work

Year: YYYY
Type: medium, duration/dimensions

---

[description paragraphs, embeds, images]
```

- `Year:` and `Type:` metadata follow the same trailing-space convention.
- Image paths **must** use a `./` prefix: `![alt](./filename.webp)`, not `![alt](filename.webp)`.
- Bare YouTube URLs become embedded players; `[text](url)` stays a plain hyperlink.

### Listings

- `writings/content.md` is **auto-generated** by `update-subpages.py` (one link per entry, newest first).
- `works/content.md` uses a **manually maintained** table (custom layout with Title / Year / Type columns). The script only generates it if the file is missing — it never overwrites an existing `works/content.md`.

## URL System

Article URLs use a Notion-style scheme: `{title-slug}-{32-char-hex-id}`.

- **Folder name** is `{initial-title-slug}-{id}` — created once, never renamed.
- **Browser URL** auto-updates to `{current-title-slug}-{id}` via `history.replaceState` after the page loads.
- **Stale URLs** (with outdated title slugs) still resolve: the root `404.html` extracts the hex ID, fetches the matching section's `articles.json` (`writings/articles.json` or `works/articles.json`), and redirects to the canonical folder.

### Adding a new article

1. Generate a 32-char hex ID: `openssl rand -hex 16`
2. Create a folder: `writings/{title-slug}-{id}/`
3. Add `content.md` inside it (with nav line, `# Title`, `Published: YYYY-MM-DD`, and `Author:`).
4. Run `python3 update-subpages.py` — regenerates `index.html`, the listings page, and `articles.json`.

### Adding a new work

1. Generate a 32-char hex ID: `openssl rand -hex 16`
2. Create a folder: `works/{title-slug}-{id}/`
3. Add `content.md` inside it (with nav line, `# Title`, `Year:`, `Type:`, and description/embeds).
4. Add a `preview.webp` image (used for hover preview on the works table).
5. Run `python3 optimize-images.py --run` to generate `preview-tiny.webp`.
6. Manually add a row to `works/content.md` (reverse chronological order).
7. Run `python3 update-subpages.py` — regenerates `index.html` and `articles.json`.

### Changing an article title

Edit the `# Title` heading in `content.md`. That's it. No folder renames or link updates needed — `replaceState` handles the URL, and `update-subpages.py` picks up the new title for the listing page.

## Images

- All images use **WebP** format. Run `python3 optimize-images.py --run` to convert JPG/JPEG/PNG → WebP, delete originals, and generate missing blur thumbnails. Requires **Pillow** (`pip install Pillow`).
- Every `.webp` gets a `*-tiny.webp` sibling (~32px wide) used as a blur placeholder. The full image fades in over the blur on load (Medium-style blur-up). Degrades gracefully if no tiny version exists.
- Works entries include a `preview.webp` (with `preview-tiny.webp`). On desktop, hovering a title in the works table shows the preview large and tilted behind the text. Disabled on touch devices.

## Markdown File Override

`app.js` supports loading a different markdown file via the `?file=yourfile.md` URL parameter. The default is `content.md`. A reference file `sample-content.md` demonstrates the supported markdown features.

## Scripts

### `update-subpages.py`

Regenerates the HTML scaffolding and content listings for both sections:

- Creates/updates `index.html` for each section and each entry folder.
- Auto-generates `writings/content.md` (entry links sorted newest-first by `Published:` date).
- Generates `works/content.md` only if missing (the custom table is manually maintained).
- Writes `writings/articles.json` and `works/articles.json` (hex-ID → folder-name maps used by `404.html` for stale-URL redirects).

### `optimize-images.py`

Converts images under `writings/` and `works/` to WebP and generates blur thumbnails:

- `python3 optimize-images.py` — dry-run preview of convertible images.
- `python3 optimize-images.py --run` — convert JPG/JPEG/PNG → WebP (quality 80), delete originals, and generate `*-tiny.webp` thumbnails (32px wide, quality 50) for every `.webp` that lacks one.
- Requires **Pillow**: `pip install Pillow`.

### `yt-scenes.py`

Extracts the YouTube thumbnail and scene-change keyframes from a video — useful for creating `preview.webp` images and reference stills.

```
python3 yt-scenes.py <youtube-url> [--threshold N] [--max-scenes N] [--output-dir DIR]
```

- Downloads the highest-resolution thumbnail.
- Downloads the video, runs scene-change detection (AdaptiveDetector), and saves one keyframe per scene as lossless PNG.
- `--threshold` controls sensitivity (lower = more scenes; default 3.0).
- `--max-scenes` caps the number of extracted scenes (evenly sampled).
- Output goes to `./yt-scenes-output/<video-title>/` by default.
- Requires: `pip install yt-dlp scenedetect[opencv] requests`

## Dependencies


| Dependency                                                                        | Used by              | Install                                    |
| --------------------------------------------------------------------------------- | -------------------- | ------------------------------------------ |
| [Marked.js](https://github.com/markedjs/marked)                                   | `app.js` (via CDN)   | loaded from jsDelivr                       |
| [marked-extended-tables](https://github.com/calculuschild/marked-extended-tables) | `app.js` (via CDN)   | `npm install` (declared in `package.json`) |
| [Pillow](https://python-pillow.org/)                                              | `optimize-images.py` | `pip install Pillow`                       |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp)                                        | `yt-scenes.py`       | `pip install yt-dlp`                       |
| [scenedetect](https://github.com/Breakthrough/PySceneDetect)                      | `yt-scenes.py`       | `pip install scenedetect[opencv]`          |
| [requests](https://docs.python-requests.org/)                                     | `yt-scenes.py`       | `pip install requests`                     |


## Acknowledgments

This project uses the following open-source libraries:

- **[Marked.js](https://github.com/markedjs/marked)** — A markdown parser and compiler. Built for speed. Licensed under [MIT](https://github.com/markedjs/marked/blob/master/LICENSE).
- **[marked-extended-tables](https://github.com/calculuschild/marked-extended-tables)** — Extends Markdown tables with column spanning, row spanning, and multi-row headers.
- **[jsDelivr](https://www.jsdelivr.com/)** — A free, fast, and reliable CDN for open-source projects. Used to serve the Marked.js library.

This site was vibecoded with [Cursor](https://cursor.sh/).