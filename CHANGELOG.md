# Changelog

Repository-level changes. Each crate keeps its own `CHANGELOG.md`.

## [Unreleased]

### Added

- Workspace scaffold for XPlanung, XBau, XBreitband, XTrasse, XRechnung,
  XBestellung and XVergabe: canonical crate, short-name alias, npm and PyPI
  binding per standard.
- Short-name aliases on npm and PyPI (`xplanung`, `xbreitband`, `xtrasse`,
  `xbestellung`, `xvergabe`; `xbau` on PyPI only, npm refuses the name),
  pure re-exports pinned to the bindings, released by `<x>-npm-v…` and
  `<x>-py-v…` tags.
- Gate, CI, and per-crate release workflow with trusted publishing to
  crates.io, npm and PyPI.
