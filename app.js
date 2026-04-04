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
                // Replace the link with an embedded player
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

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadContent);
} else {
    loadContent();
}

