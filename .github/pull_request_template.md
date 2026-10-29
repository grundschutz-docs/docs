## What this does and why

<!-- The decision behind it, not just the diff — see CONTRIBUTING.md,
     "Working with AI": syntax isn't the bar, structure is. -->

## Checklist

- [ ] `pnpm run build` succeeds
- [ ] If this touches `scripts/generate_docs.py`: ran it and read the diff of the generated `.mdx` files
- [ ] If this touches colors/`custom.css`: checked light **and** dark mode, and text still reaches 4.5:1 contrast in both
- [ ] If this touches layout: checked mobile **and** desktop (down to 320 px: tables must not be cut off)
- [ ] Any new number on the site is generated and checked by one of the `check_*()` functions in `generate_docs.py`, not hand-written
- [ ] If the generator writes a new folder: it is in `add-paths` of `.github/workflows/sync-catalog.yml` (`check_sync_paths()` fails otherwise)
