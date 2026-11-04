# Project rules

Read `README.md` ("How the docs are generated") and `CONTRIBUTING.md` before changing content. What matters most:

## Generated files: never edit by hand

`scripts/generate_docs.py` writes these; the next run overwrites a hand edit, and `.github/workflows/generated.yml`
fails the build when committed files differ from the generator output:

- `src/content/docs/` `grundschutzpp/`, `rollen/`, `vergleich/`, `zielobjekte/`, `dokumente/`, `gefaehrdungen/`
- `src/data/*.json`, `public/downloads/`

Change the generator, then run it and commit both. Hand-written pages (`impressum.mdx`, `methodik.mdx`, `befunde/`, ...)
are edited directly. Shortened meta descriptions live in `DESCRIPTION_OVERRIDES` in the generator.

Running it needs the BSI repository at the commit named in `src/data/upstream.json` (full history, not shallow) and the
`GRUNDSCHUTZPP_*` variables from `.github/workflows/generated.yml`. The generator refuses to write numbers it cannot
recompute by a second path (`check_*()` functions); do not weaken a check to make a run pass.

## Numbers and legal statements

No hand-typed figures about the catalog: they come from the generator and are checked by `test_handwritten_numbers.py`.
Legal and BSI statements need a primary source (BSIG, BSI FAQ, EU text); the BSI standard 300-1 is under the BSI terms
of use, not under CC BY-SA (see the licence line in `Footer.astro`).

## Before you call something done

1. `rm -rf dist && pnpm run build`, then check the exit code and that the log contains "All internal links are valid".
   The links validator reports its error after the "Completed" lines; do not cut the log with `head`.
2. Run the tests in `scripts/tests/`: `python3 -B scripts/tests/test_<name>.py`, `node --test scripts/tests/id-check.test.mjs`
   (Node 22: add `--experimental-strip-types`). The ones that read `dist/` skip silently without a build.
   The browser tests (`a11y.test.cjs`, `print.test.cjs`, ...) need Playwright and axe-core, see `ci.yml`.
3. Every new invariant gets a counter-test: break the thing on purpose and see the test fail.

## Accessibility

Target WCAG 2.2 AA, AAA where cheap. `a11y.test.cjs` runs axe on 36 pages and two interaction states in four variants.
Colour tokens: do not use `--sl-color-accent` for small text in the light theme (3.6:1); `--sl-color-gray-3` is tuned
for 7:1, see the comments in `src/styles/custom.css`. Wide tables and code blocks are made keyboard-reachable by
`ScrollBereiche.astro`; do not wrap them by hand.

## Architecture decisions

`adr/README.md` lists them with status. Add an ADR for a decision that someone would otherwise re-open.

## Git

Commit messages in English, no AI attribution trailer. Daily sync PRs from the bot get no CI run; review the diff and
run build plus tests locally before merging.

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)
