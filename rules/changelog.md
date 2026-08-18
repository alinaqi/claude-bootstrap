---
description: Changelog discipline — every commit ships with a CHANGELOG entry
---

## Changelog — Required for Every Commit

Every commit that changes behaviour, config, docs, or dependencies MUST update a
`CHANGELOG.md` in the same commit. No feature, fix, or refactor lands without a
changelog line.

### Rules

1. **Keep a `CHANGELOG.md`.** If none exists at the repo root (or in the package
   you're touching), create one following [Keep a Changelog](https://keepachangelog.com):
   ```markdown
   # Changelog

   ## [Unreleased]
   ### Added
   ### Changed
   ### Fixed
   ```
2. **One entry per commit.** Add a line under the matching heading
   (Added / Changed / Fixed / Removed / Security) describing *what* changed and
   *why* — the same logical change the commit captures.
3. **Same commit, not a follow-up.** The changelog edit is staged and committed
   together with the code. A commit with code changes and no changelog change is
   incomplete.
4. **Monorepos:** update the `CHANGELOG.md` closest to the changed files, and the
   root `CHANGELOG.md` if the change is user-visible at the top level.
5. **Version on release.** When cutting a release, rename `[Unreleased]` to the
   new version + date and start a fresh `[Unreleased]` block.

### Exempt (no changelog needed)

Pure whitespace/formatting, typo fixes in comments, and changes to the changelog
itself. When in doubt, add the entry.

### Before committing

- [ ] `CHANGELOG.md` has an entry for this change
- [ ] The entry is staged in the same commit as the code
