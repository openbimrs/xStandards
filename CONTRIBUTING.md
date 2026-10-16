# Contributing

Contributions are welcome. Read AGENTS.md and run the verification gate
before opening a pull request. Pull requests from outside the maintainer
team need a maintainer's approval, both to run CI and to merge.

1. Encode only facts that a public source of the standard's operator states;
   cite it in rustdoc.
2. Never add schema files, samples, code lists, or specification text. Keep
   local copies in the ignored `references/` directory.
3. Add or update a failing test before production behavior changes.
4. Run `scripts/gate.sh` and add an `[Unreleased]` entry to the changelog of
   every crate you change.

## Adding a standard

```bash
scripts/new-standard.py xfoo --name XFoo --operator "…" \
    --homepage https://… --summary "One sentence without final period"
```

Pass `--no-alias` when the short name is taken on crates.io, and
`--no-npm-alias` when only npm refuses it (as for `xbau`). Add the
standard to the tables in README.md and AGENTS.md, then run the gate.

## Releasing a crate

Every crate is versioned and released on its own by tag
`<crate>-v<version>`; `.github/workflows/release.yml` publishes it:

| Crate | Registry | Environment |
| --- | --- | --- |
| `openbim-<x>`, `<x>` | crates.io | `crates.io` |
| `openbim-<x>-wasm` | npm `@openbim/<x>` | `npmjs.com` |
| `openbim-<x>-py` | PyPI `openbim-<x>` | `pypi.org` |
| `<x>-npm` (alias, `crates/<x>/npm`) | npm `<x>` | `npmjs.com` |
| `<x>-py` (alias, `crates/<x>/python`) | PyPI `<x>` | `pypi.org` |

```bash
scripts/release-crate.py openbim-xbau --set 0.1.1           # dry run: blast radius
scripts/release-crate.py openbim-xbau --set 0.1.1 --apply   # bump manifests, changelog, lock
# review, merge to main, then
scripts/release-crate.py openbim-xbau --publish             # tag and push; CI publishes
```

An alias pins its canonical crate exactly, so every release of `openbim-<x>`
is followed by a release of `<x>`; `--apply` rewrites the pin and says so.
A binding's npm or PyPI manifest is bumped together with its Cargo.toml.
The npm and PyPI aliases carry their binding's version and pin it exactly
(the gate checks both); bump them by hand with the binding and release them
after it: `scripts/release-crate.py xbau-npm --publish`, `… xbau-py --publish`.

The workflow refuses a tag that is not on `main` or disagrees with the
manifests, waits for CI to pass on the tagged commit, and then publishes;
each environment requires a maintainer's approval. Re-running a partly
failed release skips what is already live. To rehearse, run the workflow by
hand with a tag name: it builds and tests, and publishes nothing.

### First publish of a package

- **crates.io** accepts a trusted publisher only for an existing crate. The
  `crates.io` environment holds a `CARGO_REGISTRY_TOKEN` fallback for first
  publishes. Afterwards add the trusted publisher in the crate's Settings ->
  Trusted Publishing: repository `openbimrs/xStandards`, workflow
  `release.yml`, environment `crates.io`.
- **npm** likewise: publish once with the `NPM_TOKEN` fallback in the
  `npmjs.com` environment, then add the trusted publisher on npmjs.com
  (same repository, workflow and environment `npmjs.com`) and allow
  `npm publish`, which configurations created since 2026-09-03 do not by
  default.
- **PyPI** accepts a pending trusted publisher for a project that does not
  exist yet (project `openbim-<x>`, same repository and workflow,
  environment `pypi.org`); `PYPI_API_TOKEN` is an optional fallback.

Delete each fallback token once every package it covered trusts the
workflow. Renaming `release.yml` or an environment breaks publishing until
the registries follow.

## Licensing contributions

Unless an explicitly signed agreement says otherwise, every contribution
submitted to this repository is licensed under `MIT`. Submit only work that
you have the right to license. Identify third-party material and preserve
its license, attribution, and provenance.
