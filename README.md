# Markdown Reader

A clean, Notion-style markdown reader that works as a single-page application. Simply edit the markdown file and refresh to see your changes.

## Features

- 🎨 Clean, modern design inspired by Notion
- 📱 Fully responsive layout
- 🖼️ Enhanced image handling with automatic centering
- 🎥 YouTube embed support (auto-converts YouTube links to embedded players)
- ✏️ Easy editing - just modify the markdown file

## Usage

1. Edit `content.md` with your content
2. The page automatically loads and renders the markdown
3. Use `?file=yourfile.md` in the URL to load a different markdown file

### YouTube Embeds

Simply paste a YouTube URL as a link and it will automatically be converted to an embedded player:

```markdown
https://www.youtube.com/watch?v=VIDEO_ID
```

### Images

Use standard markdown image syntax:

```markdown
![Alt text](image-url.jpg)
```

Images are automatically centered and styled.

## Local Development

To run locally, you'll need to serve the files through a web server (browsers block file:// requests for security):

**Python:**
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000/index.html`

**Node.js:**
```bash
npx http-server
```

## GitHub Pages

This repository is set up to automatically deploy to GitHub Pages via GitHub Actions. The site will be available at:

`https://[your-username].github.io/leolauhk/`

Make sure to enable GitHub Pages in your repository settings and select "GitHub Actions" as the source.

