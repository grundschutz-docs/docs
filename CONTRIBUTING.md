# Contributing

PRs welcome. For anything bigger than a bugfix — a new generator feature, a
new page outside the catalog, a layout change — open an issue first and say
what you're after. That isn't a gate, it saves you two evenings on
something that turns out not to fit or is already half-solved elsewhere.

- **`pnpm run build` must succeed** before you open a PR.
- **Generator changes need an actual run**: if you touch
  `scripts/generate_docs.py` or the catalog processing, run the script and
  look at the diff of the generated `.md` files — not just that it runs
  without errors, but whether the generated content is actually right.
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
