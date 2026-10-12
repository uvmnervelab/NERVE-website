# NERVE Lab website

Live at **https://nervelab.w3.uvm.edu**. Astro 5 + React + Tailwind, fully static.

This site also holds `publications.yaml`, the **single source of truth for publications
for both lab sites**. `../span-website` reads it at build time, so keep the two repos
side by side in `~/03_web/`.

---

## Quick reference: what do I edit?

| I want to… | Edit this | Using |
|---|---|---|
| Add a paper | `publications.yaml` (indirectly) | `pubman --doi <DOI>` |
| Fix or tweak a paper's details | `publications.yaml` | text editor, then `pubman --regenerate` |
| Add a paper's figure | `public/assets/images/figures/<key>.jpg` | drop the file in |
| Add/edit a team member | `src/content/team.yaml` | text editor |
| Add a team photo | `public/assets/people/` | drop the file in |
| Post news | `src/content/news.yaml` | text editor |
| Edit research areas | `src/content/research/*.md` | text editor |
| Change lab name, nav, hero text, social links | `src/config.ts` | text editor |
| Change UI wording/translations | `src/i18n/ui.ts` | text editor |

**Don't edit by hand:**
- `src/content/publications/*.md`. pubman generates these, and it overwrites them.
- `dist/`. This is the build output.
- `citations.bib`. It's empty on purpose (see below).

---

## Publications (pubman)

Publications are managed with **pubman**, our Python CLI
(`~/06_projects/open_source/pubman`). Configuration lives in `pubman.toml` in this
directory, so **always run pubman from here**.

```bash
cd ~/03_web/nerve-website

pubman --doi 10.xxxx/xxxxx                 # add a paper by DOI (metadata from CrossRef)
pubman --bib paper.bib                     # add from a BibTeX file
pubman --orcid 0000-0000-0000-0000         # bulk-import from an ORCID profile
pubman --doi 10.xxxx/xxxxx --category conference   # override the inferred category
pubman --regenerate                        # rebuild outputs after hand-editing the YAML
```

### Adding a paper, step by step

1. Run `pubman --doi <DOI>`. It adds an entry to `publications.yaml` and prints its
   **key** (e.g. `BaWe26`, built from the first two authors' surnames and the year).
2. Save the paper's figure as `public/assets/images/figures/<key>.jpg`.
3. Open `publications.yaml`, find the entry, and check or adjust it (see fields below).
   If you changed anything, run `pubman --regenerate`.
4. Run `npm run dev` to check it, then deploy (below). Rebuild and deploy
   `span-website` too if it's a SPAN paper.

### Useful fields in `publications.yaml`

| Field | Meaning |
|---|---|
| `category` | `peer-reviewed`, `conference`, `invited-talk` or `selected-talk`. **Only `peer-reviewed` appears on this site** (set in `pubman.toml`). |
| `month` | 1–12. Papers are sorted by month within each year. |
| `image` | Figure path, normally `/assets/images/figures/<key>.jpg`. |
| `groups` | Add `- span` to show the paper under "recent publications" on the SPAN site's home page. |
| `doi`, `journal`, `volume`, `number`, `pages`, `abstract` | Citation details. Fix them here if CrossRef got something wrong. |

### If `pubman` isn't found

pubman is installed in its own virtual environment and linked onto your PATH:

```bash
cd ~/06_projects/open_source/pubman
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .
ln -sf "$PWD/.venv/bin/pubman" ~/.local/bin/pubman
```

### About `citations.bib`

This site started from the Scholar-Lite template, which imported papers from BibTeX.
`npm run build` still runs that importer (`scripts/import-bibtex.js`), so the file
has to exist. **Leave it empty.** pubman is the real workflow.

---

## Team & news

Both are single YAML files with instructions in comments at the top. The dev server
reloads as soon as you save.

- **`src/content/team.yaml`**
  - Every entry needs a unique `id`, which is also the profile URL (`/team/<id>`).
  - `avatar` is a path like `/assets/people/jane.jpg`. Put the file in `public/assets/people/`.
  - `author_keys` lists every way the person's name appears in publications
    (e.g. `"Barrows, Anthony"`, `"Barrows, A."`). This links their papers to their profile.
  - `weight` sets the order (lower numbers come first).
  - Alumni (`role: Alumni`) appear as a plain text list with `employment` and no photo.
- **`src/content/news.yaml`**
  - Needs `id`, `title` and `date` (YYYY-MM-DD). It's sorted newest-first automatically.
  - Use `type: media` with `outlet` and `url` for press coverage.

---

## Running, building, deploying

```bash
npm install          # first time only
npm run dev          # local preview at http://localhost:4321
npm run lint         # type-check (astro check)
npm run build        # BibTeX import → astro build → search index (months come from pubman)
npm run preview      # preview the built site
```

**Deploy:** run the deploy script (works from any directory).

```bash
./scripts/deploy.sh    # builds, then rsyncs dist/ to w3_nervelab:www-root/
```

`.gitlab-ci.yml` also builds GitLab Pages on pushes to `main`.

---

## Layout

```
publications.yaml        ← publication manifest (pubman edits this)
pubman.toml              ← pubman config
src/config.ts            ← site-wide settings
src/content/             ← team.yaml, news.yaml, research/, publications/ (generated)
src/components, pages    ← Astro/React code
public/assets/           ← images served as-is (people/, images/figures/)
scripts/                 ← deploy.sh, import-bibtex.js, enrich-months.py,
                           build_manifest.py (one-time migration, no longer needed)
```
