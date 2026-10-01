## What this does and why

<!-- The decision behind it, not just the diff — see CONTRIBUTING.md,
     "Working with AI": syntax isn't the bar, structure is. -->

## Checklist

- [ ] `pnpm run build` succeeds
- [ ] If this touches `scripts/generate_docs.py`: ran it and read the diff of the generated `.mdx` files
- [ ] If this touches colors/`custom.css`: checked light **and** dark mode
- [ ] If this touches layout: checked mobile **and** desktop
- [ ] Any new number on the site is generated and checked by `check_invariants()`, not hand-written
