# Grundschutz++ Docs

The BSI ships its Grundschutz++ security catalog as a 10k+ line OSCAL JSON
file — built for SSP-generation tooling, unreadable by a human who just
wants to know what a control requires. This project turns that same JSON
into a site you'd actually want to read: full-text search, one permalink
per control, security level / effort / base threats shown inline, dark
mode, and a print-to-PDF per topic area.

This is an unofficial, independent project — not affiliated with,
endorsed by, or produced by the Bundesamt für Sicherheit in der
Informationstechnik (BSI).

## Why this exists

There's already a community-built viewer for the catalog with more visual
firepower than this site aims for — graphs, diagrams. This one is going
for something different: a clean, modern reading experience — searchable,
permalinked, comfortable to sit down with. The BSI's catalog content stays
CC BY-SA, exactly as licensed; the code here is MIT.

Past that, the pilot catalog is JSON-first by design — built for tooling
and SSP generation, not for reading. Keeping it current here means running
the generator against the upstream source automatically, not
hand-transcribing it once and letting it rot.

## Hosted instance

A hosted instance is planned — free to use, always built against the
current upstream catalog, no setup required. It runs **this** code: there
is no separate tier, no feature held back, nothing you can't run yourself.
The convenience is the hosting, not a different version of the site.

An earlier plan split the project into this repo plus a closed-source
"hosted" layer with richer components. That split was dissolved after a
day — the components live here now, under MIT like everything else. The
reasoning, including what it cost and why it was wrong, is in
[`adr/0008`](adr/0008-aufloesung-des-oss-hosted-splits.md).

## Status

The upstream catalog is in its pilot phase (April – September 2026); BSI
is expected to present it publicly at it-sa Nürnberg (October 2026). The
site tracks whatever the catalog looks like at build time — see the
in-site "Status & Zeitplan" page for the current pilot timeline.

## Getting started

```sh
pnpm install
pnpm run dev      # http://localhost:4321
pnpm run build    # production build to ./dist/
pnpm run preview  # preview the production build locally
```

Requires the pnpm version pinned in `package.json` (`packageManager`).

## How the docs are generated

The pages under `src/content/docs/grundschutzpp/` are generated, not
hand-written. `scripts/generate_docs.py` reads the BSI's
`Grundschutz++-resolved_catalog.json` (OSCAL) and renders Starlight MDX
from it — MDX rather than plain markdown so the generated pages can use
real components (`ControlMeta` for the obligation/level/effort pills,
`PdcaCycle`, the filter inputs) instead of bold-text metadata.

Locally, it expects a `Grundschutz-PlusPlus` checkout of
[`BSI-Bund/Stand-der-Technik-Bibliothek`](https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek)
as a sibling directory:

```sh
cd Grundschutz-PlusPlus && git pull
python3 ../Grundschutz-Docs/scripts/generate_docs.py
cd ../Grundschutz-Docs && pnpm run build
```

In CI, `.github/workflows/sync-catalog.yml` runs on a daily schedule,
checks the upstream catalog out directly, regenerates the docs, and opens
a pull request if anything changed — review the diff before merging (see
CONTRIBUTING.md). `.github/workflows/ci.yml` runs a production build on
every push and pull request.

## Project structure

```
.
├── adr/                       # architecture decisions, with the reasoning
├── scripts/
│   └── generate_docs.py       # OSCAL catalog → Starlight MDX
├── src/
│   ├── components/            # ControlMeta, PdcaCycle, filters, chrome
│   ├── content/docs/
│   │   ├── grundschutzpp/     # generated — one page per topic area
│   │   ├── rollen/            # generated — entry pages per role
│   │   ├── index.mdx          # homepage
│   │   ├── vergleich.mdx      # generated — old Kompendium ↔ Grundschutz++
│   │   ├── impressum.md       # legal notice template (see adr/0003)
│   │   └── datenschutz.md     # privacy policy template
│   └── styles/custom.css      # OKLCH palette, light + dark
├── astro.config.mjs           # site title, sidebar, Starlight plugins
└── .env                       # SITE_NAME (see .env.example)
```

## Contributing

See `CONTRIBUTING.md` for what's expected in a PR (build must pass,
generator changes need an actual run and diff review, check both color
schemes and both mobile/desktop layouts) and `CODE_OF_CONDUCT.md` for
community expectations.

## What's next

Not promises, just what's on the list — open an issue if you want to pick
one of these up (see `CONTRIBUTING.md`):

- Cross-references to the old IT-Grundschutz-Kompendium controls each new
  control replaces (old ID + title + link, via BSI's own mapping file)
- Filtering the catalog by theme, using the tags already in the source
  data but not yet exposed in the UI
- An OSCAL explainer page — what it is, and why a German agency adopted a
  NIST-originated format instead of building its own
- A real English translation of the catalog content (the i18n scaffold
  already works, the translation itself doesn't exist yet)

## License

- **Code**: MIT — see `LICENSE`.
- **Catalog content** (the Grundschutz++ text rendered under
  `src/content/docs/grundschutzpp/`): CC BY-SA 4.0, © BSI-Bund, per the
  upstream catalog's own license. This site's generated pages inherit that
  license from their source.

The BSI-OSCAL catalog itself follows [OSCAL](https://pages.nist.gov/OSCAL/),
a standard originating from NIST that the BSI adopted rather than building
a proprietary format.
