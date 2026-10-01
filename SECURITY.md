# Security Policy

## Scope

This covers vulnerabilities in **this site's code** — the Astro build,
the generator script, the GitHub Actions workflows. It does not cover
problems with the Grundschutz++ catalog's own content (wrong text,
contradictions, bad mappings) — those go in the public
[findings register](https://github.com/grundschutz-docs/docs#readme)
(`/befunde/` on the site) instead, not here.

## Supported versions

There isn't a version matrix to maintain — this is a static docs site
built fresh from `main` on every deploy, not a library with multiple
maintained release branches. A fix lands on `main` and is live on the
next build.

## Reporting a vulnerability

Please do not open a public issue for a security problem. Instead, use
GitHub's private
[**Report a vulnerability**](https://github.com/grundschutz-docs/docs/security/advisories/new)
button (Security tab → Advisories), or email
bruno.deanoz@protonmail.com directly.

This is a one-person hobby project (see `ueber.mdx` / the site's "Über
diese Seite" page) — there's no SLA, but a security report gets looked
at before anything else in the queue.
