# Contributing

Non-code input counts just as much as a PR — a different reading of a
requirement, a gap you noticed, an open question. There's a low-friction
[issue template](https://github.com/grundschutz-docs/docs/issues/new?template=catalog_finding.yml)
for exactly that ("Catalog finding"). Worst case if it doesn't fit or is
already known: I'll say so and why — no public callout, no drawn-out fight.

PRs welcome. For anything bigger than a bugfix — a new generator feature, a
new page outside the catalog, a layout change — open an issue first and say
what you're after. That isn't a gate, it saves you two evenings on
something that turns out not to fit or is already half-solved elsewhere.

- **`pnpm run build` must succeed** before you open a PR.
- **Generator changes need an actual run**: if you touch
  `scripts/generate_docs.py` or the catalog processing, run the script and
  look at the diff of the generated `.mdx` files — not just that it runs
  without errors, but whether the generated content is actually right.
  You'll need `python3` for this (stdlib only, no `pip install` or venv —
  see README.md's "How the docs are generated" for the exact invocation
  against a `Grundschutz-PlusPlus` checkout).
- **Look at it, don't just build it.** A green build only proves nothing
  crashed, not that it looks right — see "Green isn't the same as right"
  below.
- **Check light and dark mode** for anything touching colors or
  `custom.css`. The OKLCH palette is defined separately for both; a fix
  for one can silently break the other.
- **Check mobile and desktop** for layout changes. Sidebar, header, and
  table of contents behave differently above/below `50rem` and `72rem` —
  testing on desktop alone isn't enough.
- **Keep it lightweight.** This site is meant to be self-hostable via
  Docker or a systemd service, without heavy runtime dependencies. New
  external services, CDN dependencies, or heavy client frameworks need a
  real justification, not a default yes.

## Numbers on the site

Any figure the site states about the catalog — "1000 requirements", "149 of
them are MUSS", the per-practice counts, the stats on the homepage — must be
**generated from the catalog and checked by `check_invariants()`** in
`scripts/generate_docs.py`. Never hand-write one, and never add a new figure
without a check alongside it. A wrong number is worse than a missing one:
nothing about it looks broken.

The rule that check has to follow, and the reason it exists:

> **Verify each number by a second, independent path.**

This is not theoretical. On 2026-09-30 the Geschäftsführung page claimed
"123 of 874 requirements are MUSS" — the real figures are 149 of 1000, and
the table below it was missing 26 MUSS requirements on the page that is
specifically about legal obligation. Every build was green the whole time,
and the link validator was happy.

It survived because the heading and the table were computed by the *same*
function. They agreed with each other, and that agreement looked like
confirmation when it was only the shared bug. The underlying mistake was an
assumption written into a docstring — that parent controls are structural
containers rather than requirements. In this catalog all 1000 nodes carry
their own `statement` and modal verb, parents included.

So `check_invariants()` reads the **written files back** and compares them
against the catalog: anchors in the generated pages, `<tr>` rows in the MUSS
table and the Baustein pages, the figures in `landing.json`. A check that
walks the same code path as the renderer proves nothing — if you add one,
make sure it counts a different way.

To confirm a check works, break the thing it guards on purpose and watch the
generator fail. If it still passes, the check is decoration.

## When the upstream catalog changes

The catalog this site renders lives in
[`BSI-Bund/Stand-der-Technik-Bibliothek`](https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek)
and moves on its own schedule. `.github/workflows/sync-catalog.yml` picks
that up daily and opens a PR. Before merging one:

1. **Re-run the generator and read the diff**, don't just trust the green
   check. A catalog edit can silently change what a requirement *says*.
2. **Check the prop schema.** The generator reads `sec_level`,
   `effort_level`, `threats` and `modal_verb` off the controls. A renamed
   or newly added prop won't fail the build — it'll just quietly stop
   appearing on the page.
3. **Watch for MDX-hostile prose.** `mdx_safe()` escapes `{`, `}` and `<`
   in catalog text after parameter substitution. Without it a sentence
   like "Latenz < Antwortzeit" breaks the build. New editions can
   introduce new problem characters.
4. **Check the old-Kompendium links.** `bsi-kompendium-2023-bausteine.json`
   maps 111 Baustein IDs to BSI's own PDF URLs and backs the "Vorgänger"
   cross-references (see `adr/0005`). It was scraped once, by hand — BSI's
   bot protection blocks simple scripted scraping — so a new Kompendium
   edition means re-doing that by hand. See `_method` inside the file.
5. **Sanity-check the mapping direction.** `subset-of` means the old
   requirement is contained in the new one; `superset-of` means the new
   one is narrower. This was wrong once already (see `adr/0005`), and it's
   the kind of error a build never catches.

## Working with AI

Using AI to work on a PR — including the actual code — is explicitly fine
here. Large parts of this site were built exactly that way. No disclosure
required, no "explain every line" gate.

So what follows isn't a warning, it's what I actually look at in review,
written down so you know it beforehand.

- **You're the director, the AI is the worker.** It executes; the decision
  stays yours. That's not a dig at the tools — it follows from a
  structural limit: a model has no need of its own. A design decision is
  always the answer to a problem somebody actually *has* — "this bothered
  me, so it had to look like this" — and that problem is yours. The
  question about a PR is never "did you type this yourself", it's "what
  does this make possible, and why in this form".
- **Syntax isn't the bar, structure is.** Whether a CSS rule is correct is
  something you can look up. Whether a new page belongs in the generator
  (and gets rewritten on every run) or should be its own hand-maintained
  file (like `impressum.md`) is a decision that needs someone who wants
  something. Concretely: do you know what *capability* your change
  actually alters — not just the diff lines? Does it belong in the
  generator or next to it? Does a slug rename silently break the sidebar
  config or external links?
- **Green isn't the same as right.** A build that succeeds only proves
  nothing crashed. Several real bugs in this site (duplicate headings, a
  footer that wasn't visible, banner text with no space before the link)
  were green on every build and only showed up when someone actually
  looked. For a bugfix: put the bug back first, confirm it reproduces,
  then fix it again and confirm it's gone.

And if a contribution doesn't fit as-is, that's a conversation, not a
wall — say what you were after, I'll say what doesn't fit and why, and
there's usually a way to make it work anyway.
