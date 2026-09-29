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

No readable cross-reference existed anywhere — not in the official repo,
not from BSI itself. The pilot catalog is JSON-first by design, and that's
the right call for tooling, but it leaves nothing a human can skim to
answer "what does this control actually ask of me." This project reads
the same source of truth and renders it for that use case instead, kept
current automatically rather than hand-transcribed once and left to rot.

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
`Grundschutz++-resolved_catalog.json` (OSCAL) and renders Starlight
markdown from it.

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
├── scripts/
│   └── generate_docs.py       # OSCAL catalog → Starlight markdown
├── src/
│   ├── components/            # Hero, Footer, Banner, theme toggle, ...
│   ├── content/docs/
│   │   ├── grundschutzpp/     # generated — one page per topic area
│   │   ├── index.mdx          # homepage
│   │   ├── impressum.md       # legal notice (German law requires this)
│   │   └── datenschutz.md     # privacy policy
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
