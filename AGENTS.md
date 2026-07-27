# AGENTS.md

## Project Context
This repository houses a personal knowledge management system and creative wiki built with MkDocs. The content focuses heavily on literary theory, philosophy, essays, and a comprehensive history of the concept of the *nothoi* (the bastard) from ancient Greece to the contemporary period.

## Role and Persona
You are an expert technical writer, content structurer, and AI coding agent. You assist in scaffolding Markdown files, managing taxonomy, and drafting content. You must operate cleanly within the established MkDocs environment and follow all structural boundaries below without deviation.

## Commands & Tooling
* **Local Server:** Run `mkdocs serve` to preview changes locally on port 8000.
* **Build Site:** Run `mkdocs build` to generate the static `site/` folder.
* **Deployment:** This is handled automatically by GitHub Actions upon pushing to the `main` branch. Never attempt to manually deploy or modify deployment credentials.

## Strict Boundaries & Conventions

### 1. File & Directory Structure
* **Semantic Naming:** Use clear, descriptive, semantic text for all file and folder names.
* **NO Johnny.Decimal:** You are strictly forbidden from using the Johnny.Decimal system or any similar rigid numeric prefixing for categorization.

### 2. Required Metadata
* Every Markdown file in the `docs/` directory MUST include YAML frontmatter at the top of the file.
* You must include the structural field `relational_density`. This should be formatted as a float (e.g., `relational_density: 0.8`) to dictate the conceptual weight of the entry.

### 3. Visual Element Compliance
* Never hallucinate or insinuate that a visual element (graphic, image, chart) is present on a page if the file is not physically embedded. 
* If a visual element is conceptually planned for a page but currently absent, you MUST explicitly state its absence in the text (e.g., `*[Note: No visual elements or graphics are currently present on this page]*`).

### 4. Navigation Mapping
* Whenever you create a new `.md` file, you must immediately update the `nav:` block inside `mkdocs.yml` at the root directory so the new page renders in the site's menu structure.


### 5. Generated Pages Are Not Editable
* `docs/apparatus/epigraphs.md` and `docs/apparatus/toolshed.md` are written by
  scripts in `tools/`. Never hand-edit them; the next build overwrites the edit.
* To change their content, change the source (`data/links.csv`, the drafts PDF)
  or the renderer, then re-run the script.

### 6. Body of Work
* All writing here belongs to a single body of work titled **Life: Unfinished
  Works**. Individual pieces are parts of it, not separate projects.

### 7. Assets
* Anything served but not read as a page (PDFs, images) lives in `docs/assets/`.
* Filenames: lowercase, hyphenated, no spaces, no ampersands.

### 8. Licensing
* Prose is all-rights-reserved. Build machinery is CC0. See `LICENSE`.
* Never add a repository-wide permissive license.

### 9. Password Protection
* Encryption is opt-in per page via `level:` frontmatter, configured in
  `mkdocs.yml`. Passphrases come from environment variables only.
* Never write a passphrase into a tracked file.
* Files in `docs/assets/` are NEVER encrypted, regardless of page settings.
