# Claude HTML Documentation Style Guide

Instructions for creating consistent `claude.html` documentation files.

---

## Color Palette

Use only black, gray, and light blue:

```css
:root {
    --bg-primary: #0a0a0a;      /* Main background - near black */
    --bg-secondary: #111111;    /* Sidebar, tables, cards */
    --bg-card: #181818;         /* Table headers, info boxes */
    --bg-hover: #1e1e1e;        /* Hover states */
    --text-primary: #d0d0d0;    /* Main text */
    --text-secondary: #606060;  /* Secondary text, labels */
    --text-muted: #404040;      /* Muted text */
    --accent: #5c9fd4;          /* Light blue - for emphasis only */
    --accent-dim: #3a6a8a;      /* Dimmed accent for borders */
    --code-bg: #0d0d0d;         /* Code blocks */
    --border: #252525;          /* Borders */
}
```

**Rules:**
- NO red, orange, or warm colors
- Use `--accent` (light blue) sparingly for:
  - h3 headings
  - Active tabs
  - Code inline elements
  - Card titles
  - TOC hover/active states
- All other text uses grays

---

## Layout Structure

```
┌─────────────────────────────────────────────────┐
│  SIDEBAR (fixed)  │  MAIN CONTENT               │
│  280px width      │  flex: 1, max-width: 1000px │
│                   │                             │
│  - TOC title      │  - h1 Title                 │
│  - Link items     │  - Subtitle                 │
│  - Sub-items      │  - Sections with id=""      │
│    (indented)     │  - Tables                   │
│                   │  - Code blocks              │
│                   │  - Tabs (if needed)         │
└─────────────────────────────────────────────────┘
```

---

## Required Sections

1. **Overview** - Location, purpose, quick reference table
2. **Architecture** - ASCII diagram showing structure
3. **Components** - Details for each class/module (use tabs if multiple)
4. **Usage Examples** - Code snippets
5. **Inheritance Hierarchy** - ASCII tree diagram
6. **Design Patterns** - Grid of cards
7. **Dependencies** - Table of dependencies

---

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Module Name] - [Short Description]</title>
    <style>
        /* Include full CSS from color palette and components */
    </style>
</head>
<body>
    <!-- Sidebar / Table of Contents -->
    <nav class="sidebar">
        <h2>Contents</h2>
        <ul class="toc">
            <li><a href="#overview">Overview</a></li>
            <li><a href="#architecture">Architecture</a></li>
            <li><a href="#components">Components</a></li>
            <li><a class="sub" href="#component1">Component1</a></li>
            <li><a class="sub" href="#component2">Component2</a></li>
            <li><a href="#usage">Usage Examples</a></li>
            <li><a href="#hierarchy">Inheritance Hierarchy</a></li>
            <li><a href="#patterns">Design Patterns</a></li>
            <li><a href="#dependencies">Dependencies</a></li>
        </ul>
    </nav>

    <!-- Main Content -->
    <main class="main">
        <h1>[Module Name]</h1>
        <p class="subtitle">[Short Description]</p>

        <section id="overview">
            <h2>Overview</h2>
            <div class="info-box">
                <p><strong>Location:</strong> <code>[path]</code></p>
                <p><strong>Purpose:</strong> [description]</p>
            </div>
            <!-- Quick reference table -->
        </section>

        <section id="architecture">
            <h2>Architecture</h2>
            <div class="diagram">[ASCII diagram]</div>
        </section>

        <section id="components">
            <h2>Components</h2>
            <!-- Tabs if multiple components -->
            <div class="tabs">
                <div class="tab active" onclick="showTab('tab1')">Tab1</div>
                <div class="tab" onclick="showTab('tab2')">Tab2</div>
            </div>
            <div id="tab1" class="tab-content active">...</div>
            <div id="tab2" class="tab-content">...</div>
        </section>

        <!-- More sections... -->
    </main>

    <script>
        /* Include tab switching and TOC highlight scripts */
    </script>
</body>
</html>
```

---

## CSS Components

### Sidebar
```css
.sidebar {
    width: 280px;
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
    padding: 1.5rem;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
}

.toc { list-style: none; }
.toc a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.9rem;
    display: block;
    padding: 0.4rem 0.75rem;
    border-radius: 4px;
    transition: all 0.2s;
}
.toc a:hover {
    color: var(--accent);
    background: var(--bg-hover);
}
.toc .sub {
    padding-left: 1.5rem;
    font-size: 0.85rem;
}
```

### Main Content
```css
.main {
    margin-left: 280px;
    flex: 1;
    padding: 2rem 3rem;
    max-width: 1000px;
}
```

### Tables
```css
table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-secondary);
    border-radius: 6px;
    overflow: hidden;
    font-size: 0.9rem;
}
th {
    background: var(--bg-card);
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
tr:hover td { background: var(--bg-hover); }
```

### Tabs
```css
.tabs {
    display: flex;
    border-bottom: 1px solid var(--border);
    margin: 1.5rem 0 0;
}
.tab {
    padding: 0.75rem 1.25rem;
    cursor: pointer;
    color: var(--text-secondary);
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
.tab.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
}
.tab-content { display: none; padding: 1.5rem 0; }
.tab-content.active { display: block; }
```

### Code Blocks
```css
code {
    background: var(--code-bg);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 0.85rem;
    color: var(--accent);
}
pre {
    background: var(--code-bg);
    padding: 1rem 1.25rem;
    border-radius: 6px;
    border: 1px solid var(--border);
}
pre code { padding: 0; background: none; color: var(--text-primary); }

/* Syntax highlighting - muted colors */
.keyword { color: #7aa2c9; }
.type { color: #a0a0a0; }
.string { color: #6a8759; }
.comment { color: #454545; }
```

### Diagrams
```css
.diagram {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    white-space: pre;
    overflow-x: auto;
    color: var(--text-secondary);
}
```

### Cards Grid
```css
.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}
.card {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem;
}
.card h4 { color: var(--accent); font-size: 0.95rem; }
.card p { color: var(--text-secondary); font-size: 0.9rem; }
```

### Info Box
```css
.info-box {
    background: var(--bg-card);
    border-left: 3px solid var(--accent-dim);
    padding: 1rem 1.25rem;
    border-radius: 0 6px 6px 0;
}
```

---

## JavaScript

### Tab Switching
```javascript
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}
```

### TOC Scroll Highlighting
```javascript
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        const link = document.querySelector(`.toc a[href="#${id}"]`);
        if (link) {
            if (scrollPos >= top && scrollPos < top + height) {
                link.style.color = 'var(--accent)';
                link.style.background = 'var(--bg-hover)';
            } else {
                link.style.color = '';
                link.style.background = '';
            }
        }
    });
});
```

---

## Checklist

Before finalizing, verify:

- [ ] Color palette uses only black, gray, light blue
- [ ] Backward should be in dark themes, and content (text, lines) in very bright.
- [ ] Fixed sidebar with clickable TOC
- [ ] Smooth scrolling enabled (`html { scroll-behavior: smooth; }`)
- [ ] All sections have `id` attributes matching TOC links
- [ ] Sub-items in TOC are indented with class `sub`
- [ ] Tables have uppercase headers with letter-spacing
- [ ] Code blocks use monospace font with muted syntax colors
- [ ] Tabs work correctly (if used)
- [ ] TOC highlights current section on scroll
- [ ] Info box at top with Location and Purpose
- [ ] ASCII diagrams for architecture and hierarchy
- [ ] Design patterns in 2-column grid cards
