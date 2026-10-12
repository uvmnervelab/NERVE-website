# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm install              # Install dependencies
npm run dev              # Start dev server (http://localhost:4321/mockup)
npm run build            # Import BibTeX → build site → run Pagefind indexing
npm run preview          # Preview production build
npm run import-bibtex    # Parse citations.bib into src/content/publications/*.md only
npm run lint             # Type-check with astro check
```

No test runner is configured.

## Architecture

**Astro 5 + React + Tailwind CSS v4** static site for the NERVE Lab at UVM. Based on the Scholar-Lite template. No SSR — all pages pre-rendered at build time.

### Build Pipeline

```
citations.bib
    → scripts/import-bibtex.js  (parses BibTeX, writes to src/content/publications/)
    → Astro build               (static HTML generation, Semantic Scholar API for citation counts)
    → pagefind --site dist      (search index)
```

The `import-bibtex.js` script is the authoritative source of publication content. Do not hand-edit files in `src/content/publications/` — they will be overwritten on the next build. Edit `citations.bib` instead.

### Publication Management (pubman)

`pubman.toml` at the repo root configures the **pubman** CLI (see `~/06_projects/open_source/pubman`). Running `pubman --doi <DOI>` adds a new entry to `publications.yaml` (the manifest) and regenerates BibTeX and Astro Markdown output. The `import-bibtex` script and pubman's `astro_md` generator are parallel paths for the same end result.

pubman is installed in its own venv (`~/06_projects/open_source/pubman/.venv`, editable install) and exposed on PATH via a symlink at `~/.local/bin/pubman`. If `pubman` is not found, recreate the venv: `python3 -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -e .` from the pubman repo, then re-link.

### Content Collections

Nine collections defined in `src/content.config.ts` with Zod schemas:

| Collection | Location | Key fields |
|---|---|---|
| `publications` | `src/content/publications/` | title, authors[], year, venue, type, links, cover, featured, badges[], groups[] |
| `team` | `src/content/team.yaml` | id, name, role, avatar, author_keys[], weight (sort order) |
| `news` | `src/content/news.yaml` | id, title, date, summary |
| `research` | `src/content/research/` | title, description, cover, order |
| `books` | `src/content/books/` | — |
| `patents` | `src/content/patents/` | status (Granted/Pending/Filed) |
| `softwares` | `src/content/softwares/` | — |
| `honors` | `src/content/honors/` | — |
| `activities` | `src/content/activities/` | — |

**Team & News editing**: Unlike publications, `team` and `news` are hand-authored — each is a single YAML manifest (`src/content/team.yaml`, `src/content/news.yaml`) read via Astro's `file()` loader (see `src/content.config.ts`). Edit the YAML directly; `npm run dev` hot-reloads. Every entry needs a unique `id` (the team `id` is also the profile URL slug, `/team/<id>`). Team avatars are plain public paths (`/assets/people/<file>`) served from `public/assets/people/` — no Astro `image()` optimization, no relative paths.

**Team → Publication linking**: Each team member has an `author_keys` array (e.g., `["Barrows, Anthony", "Barrows, A."]`) that matches against publication author strings. This drives the author avatar display on publication cards.

### Key Configuration

- **`src/config.ts`** — Central site config: lab name, university, nav items, hero text, i18n toggle, social links. Start here for branding or nav changes.
- **`astro.config.mjs`** — Base path `/mockup`, React + Tailwind integrations, compressed HTML, inline stylesheets, 10KB asset inlining.

### Styling

Tailwind CSS v4 via `@tailwindcss/vite`. Component-level Tailwind classes in `.astro` files. Global styles and custom scrollbar in `src/styles/global.css`. React components (`.tsx`) are used where client-side interactivity is needed.

### i18n

`src/i18n/` provides 8-language support (EN, ZH, JA, KO, FR, DE, ES, RU). Translations live in `src/i18n/ui.ts` (~600+ keys). Language is persisted in `localStorage` and switched client-side. Enable/disable in `src/config.ts`.

### Deployment

Deployed to GitHub Pages. Base path is `/mockup` (configured in `astro.config.mjs`).
