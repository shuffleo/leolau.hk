# Agent notes

## Mixed HTML + Markdown

Some content intentionally mixes raw HTML inside Markdown (e.g. `works/content.md` table rows that use `<a … data-preview="…">` for external hover previews).

- Treat that mix as intentional, not as messy markup to clean up.
- Do **not** rewrite HTML anchors into “cleaner” Markdown links, or otherwise normalize mixed HTML/Markdown, without asking first.
- When editing nearby text, leave the HTML attributes and structure intact unless the user explicitly asks to change them.
