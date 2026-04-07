// Default markdown file to load (in the same directory as this HTML file)
const DEFAULT_MD_FILE = 'content.md';

let markedTablesConfigured = false;

function getExtendedTablesPluginFactory() {
    if (typeof window === 'undefined') return null;

    // Support different UMD/global export names.
    const direct = window.extendedTables || window.markedExtendedTables;
    if (typeof direct === 'function') return direct;

    if (direct && typeof direct.default === 'function') return direct.default;

    return null;
}

function configureMarkedExtensions() {
    if (markedTablesConfigured || typeof marked === 'undefined') return;

    const extendedTablesFactory = getExtendedTablesPluginFactory();
    if (typeof extendedTablesFactory === 'function') {
        marked.use(extendedTablesFactory());
    }

    markedTablesConfigured = true;
}

// Extract YouTube video ID from various URL formats
function getYouTubeId(url) {
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
        /youtube\.com\/watch\?.*v=([^&\n?#]+)/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) return match[1];
    }
    return null;
}

// Convert YouTube links to embedded players
function processYouTubeEmbeds(html) {
    // Create a temporary container to work with the HTML
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    // Find all links
    const links = temp.querySelectorAll('a');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href) {
            const videoId = getYouTubeId(href);
            if (videoId) {
                const text = link.textContent.trim();
                const looksLikeURL = /^https?:\/\//.test(text) || /^(www\.)?youtu/.test(text);
                if (!looksLikeURL) return;

                const embedDiv = document.createElement('div');
                embedDiv.className = 'youtube-embed';
                embedDiv.innerHTML = `<iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
                link.parentNode.replaceChild(embedDiv, link);
            }
        }
    });
    
    return temp.innerHTML;
}

// Improve image handling
function improveImageHandling(html) {
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    // Find all images and ensure they're properly styled
    const images = temp.querySelectorAll('img');
    images.forEach(img => {
        // Add loading="lazy" for better performance
        img.setAttribute('loading', 'lazy');
        // Ensure images are centered if they're in a paragraph
        if (img.parentElement.tagName === 'P') {
            img.parentElement.style.textAlign = 'center';
        }
    });
    
    return temp.innerHTML;
}

// Render markdown
function renderMarkdown(content) {
    const contentDiv = document.getElementById('content');
    if (typeof marked !== 'undefined') {
        configureMarkedExtensions();
        // Configure marked options
        marked.setOptions({
            breaks: true,
            gfm: true
        });
        let html = marked.parse(content);
        
        // Process YouTube embeds
        html = processYouTubeEmbeds(html);
        
        // Improve image handling
        html = improveImageHandling(html);
        
        contentDiv.innerHTML = html;
    } else {
        contentDiv.innerHTML = '<p>Error: Marked.js library failed to load.</p>';
    }
    contentDiv.classList.add('loaded');
    highlightActiveNav();
    updateUrlSlug();
    initHoverPreviews();
}

// Load markdown from file
function loadContent() {
    const urlParams = new URLSearchParams(window.location.search);
    // Allow override via URL parameter, otherwise use default file
    const mdFile = urlParams.get('file') || DEFAULT_MD_FILE;
    
    fetch(mdFile)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load ${mdFile}. Make sure the file exists in the same directory.`);
            }
            return response.text();
        })
        .then(text => renderMarkdown(text))
        .catch(error => {
            const contentDiv = document.getElementById('content');
            contentDiv.innerHTML = 
                `<div style="padding: 2em; color: #d32f2f;">
                    <h2>Error loading markdown file</h2>
                    <p><strong>${error.message}</strong></p>
                    <p>Make sure you have a file named <code>${mdFile}</code> in the same directory as this HTML file.</p>
                    <p>You can also specify a different file using the URL parameter: <code>?file=yourfile.md</code></p>
                </div>`;
            contentDiv.classList.add('loaded');
        });
}

function highlightActiveNav() {
    var path = window.location.pathname;
    var section = 'ABOUT';
    if (/\/works(\/|$)/.test(path)) section = 'WORKS';
    else if (/\/writings(\/|$)/.test(path)) section = 'WRITINGS';

    var contentDiv = document.getElementById('content');
    var firstP = contentDiv && contentDiv.querySelector('p');
    if (!firstP) return;

    var links = firstP.querySelectorAll('a');
    links.forEach(function (link) {
        if (link.textContent.trim() === section) {
            link.innerHTML = '<strong>\uD83D\uDD76\uFE0F ' + link.textContent.trim() + '</strong>';
        }
    });
}

function initHoverPreviews() {
    var hasHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (!hasHover) return;

    var ID_RE = /[0-9a-f]{32}\/?$/;
    var links = document.querySelectorAll('table a');
    var previewLinks = [];
    links.forEach(function (link) {
        var href = link.getAttribute('href');
        if (href && ID_RE.test(href)) {
            previewLinks.push(link);
        }
    });
    if (!previewLinks.length) return;

    var img = document.createElement('img');
    img.className = 'hover-preview';
    document.body.appendChild(img);

    var cache = {};
    previewLinks.forEach(function (link) {
        var href = link.getAttribute('href').replace(/\/?$/, '/');
        var src = href + 'preview.webp';
        var preload = new Image();
        preload.src = src;
        cache[src] = preload;
    });

    previewLinks.forEach(function (link) {
        var href = link.getAttribute('href').replace(/\/?$/, '/');
        var src = href + 'preview.webp';
        var angle = (Math.random() * 30 - 15).toFixed(1);
        link.addEventListener('mouseenter', function () {
            var rect = link.getBoundingClientRect();
            var scrollY = window.scrollY || document.documentElement.scrollTop;
            img.style.left = rect.left + rect.width / 2 + 'px';
            img.style.top = rect.top + scrollY + rect.height / 2 + 'px';
            img.style.transform = 'translate(-50%, -50%) rotate(' + angle + 'deg)';
            img.src = src;
            img.classList.add('visible');
        });
        link.addEventListener('mouseleave', function () {
            img.classList.remove('visible');
            img.removeAttribute('src');
        });
    });
}

function updateUrlSlug() {
    var path = window.location.pathname.replace(/\/+$/, '');
    var idMatch = path.match(/([0-9a-f]{32})$/);
    if (!idMatch) return;

    var contentDiv = document.getElementById('content');
    var h1 = contentDiv && contentDiv.querySelector('h1');
    if (!h1) return;

    var slug = h1.textContent.trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
    var id = idMatch[1];
    var newFolder = slug + '-' + id;

    var base = path.substring(0, path.lastIndexOf('/'));
    var newPath = base + '/' + newFolder + '/';
    if (newPath !== window.location.pathname) {
        history.replaceState(null, '', newPath);
    }
}

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadContent);
} else {
    loadContent();
}

