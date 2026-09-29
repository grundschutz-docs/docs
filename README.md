# Grundschutz++ Docs

A readable, searchable rendering of the BSI's Grundschutz++ OSCAL catalog —
the successor to the IT-Grundschutz-Kompendium, currently in its pilot
phase. This is an unofficial, independent project. It is not affiliated
with, endorsed by, or produced by the Bundesamt für Sicherheit in der
Informationstechnik (BSI).

The BSI publishes the catalog as machine-oriented OSCAL JSON, built for
tooling and SSP generation, not for reading. This site generates
human-readable pages from that same source: 20 topic areas across 6
management phases (a PDCA cycle), each control shown with its security
level, effort, and base threats — searchable, with a permalink per control.

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

## License

- **Code**: MIT — see `LICENSE`.
- **Catalog content** (the Grundschutz++ text rendered under
  `src/content/docs/grundschutzpp/`): CC BY-SA 4.0, © BSI-Bund, per the
  upstream catalog's own license. This site's generated pages inherit that
  license from their source.

The BSI-OSCAL catalog itself follows [OSCAL](https://pages.nist.gov/OSCAL/),
a standard originating from NIST that the BSI adopted rather than building
a proprietary format.
