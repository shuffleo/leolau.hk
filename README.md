# Personal Site

This is the repository for my personal website.

**Visit the live site: [leolau.hk](https://leolau.hk)**

This is a clean, Notion-style markdown reader built as a multi-page application. The site automatically loads and renders markdown content.

## Writings

- My writings are organised with a homepage at `writings/index.html` and articles at `writings/<folder>/index.html`, each paired with a local `content.md`.
- Article folders follow a strict date-plus-slug pattern: `YYYY[-MM-DD]-slug` (regex: `^(?P<pub_date>\d{4}(?:-\d{2}-\d{2})?)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$`).
- Run `python3 update-writings.py` to regenerate the writings homepage and refreshes `writings/content.md` into a simple chronological list: `# Writings`.

## Acknowledgments

This project uses the following open-source libraries:

- **[Marked.js](https://github.com/markedjs/marked)** - A markdown parser and compiler. Built for speed. Licensed under [MIT](https://github.com/markedjs/marked/blob/master/LICENSE).
- **[jsDelivr](https://www.jsdelivr.com/)** - A free, fast, and reliable CDN for open-source projects. Used to serve the Marked.js library.

This site was vibecoded with [Cursor](https://cursor.sh/).