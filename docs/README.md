# mighty-joe-black

Source for **Creative Wiki** — <https://catfish-toesuckers-what.web.app/>

A working archive rather than a finished publication: literary theory,
philosophy, essays, and an ongoing history of the *nothoi* — the bastard —
from classical Athens to the present.

## Layout

| Path | What lives there |
|---|---|
| `docs/` | All page content. Markdown only; everything here becomes a URL. |
| `docs/assets/` | Images, PDFs, anything served but not read as a page. |
| `mkdocs.yml` | Site config and navigation. New page ⇒ new `nav:` entry. |
| `requirements.txt` | Pinned build toolchain. |
| `.github/workflows/` | Build on push to `main`, deploy to Firebase Hosting. |
| `.agents/` `.claude/` | Agent skill definitions. Not published. |
| `AGENTS.md` | Working conventions for any agent editing this repo. |

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
mkdocs build --strict # fails loudly on broken links / bad nav
```

## Deploying

Push to `main`. GitHub Actions builds and deploys. Open a pull request
instead and Firebase returns a temporary preview URL — useful for showing
a draft to one reader without publishing it.

## Conventions

- Every file in `docs/` carries YAML frontmatter.
- Semantic filenames. No numeric prefixes, no Johnny.Decimal.
- Never claim a visual element is present on a page unless it is embedded.

## Licensing

The code and configuration here are CC0-1.0. **The prose, drafts, and
research notes are not** — they remain © John L. Roapes, all rights
reserved. See `LICENSE` and the notice at the top of `docs/index.md`.
