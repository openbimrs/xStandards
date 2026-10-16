# xStandards

OpenBIM.rs implementations of the German public-sector **X-standards** for
planning, building permits, infrastructure, procurement and invoicing, each
as its own Rust crate with JavaScript (npm) and Python (PyPI) bindings.

**Status: scaffold.** Every crate states which standard it implements and is
wired for release; reading, writing and validating documents is not
implemented yet.

| Standard | Operator | Rust | Alias | npm | PyPI |
| --- | --- | --- | --- | --- | --- |
| [XPlanung](https://xleitstelle.de/xplanung) — spatial and land-use plans (XPlanGML) | XLeitstelle Planen und Bauen | `openbim-xplanung` | `xplanung` | `@openbim/xplanung` | `openbim-xplanung` |
| [XBau](https://xleitstelle.de/xbau) — building-permit messages, incl. XBau core module | XLeitstelle Planen und Bauen | `openbim-xbau` | `xbau` | `@openbim/xbau` | `openbim-xbau` |
| [XBreitband](https://xleitstelle.de/xtrassexbreitband) — permits for broadband and civil works (XBau-Tiefbau) | XLeitstelle Planen und Bauen | `openbim-xbreitband` | `xbreitband` | `@openbim/xbreitband` | `openbim-xbreitband` |
| [XTrasse](https://xleitstelle.de/xtrassexbreitband) — planned line routes, built on XPlanung | XLeitstelle Planen und Bauen | `openbim-xtrasse` | `xtrasse` | `@openbim/xtrasse` | `openbim-xtrasse` |
| [XRechnung](https://xeinkauf.de/xrechnung/) — CIUS of the EN 16931 e-invoice | KoSIT | `openbim-xrechnung` | — ¹ | `@openbim/xrechnung` | `openbim-xrechnung` |
| [XBestellung](https://xeinkauf.de/xbestellung/) — electronic purchase orders | KoSIT | `openbim-xbestellung` | `xbestellung` | `@openbim/xbestellung` | `openbim-xbestellung` |
| XVergabe — e-procurement platform interface | IT-Planungsrat | `openbim-xvergabe` | `xvergabe` | `@openbim/xvergabe` | `openbim-xvergabe` |

¹ The crates.io name `xrechnung` belongs to another project.

Short-name aliases (`xbau`, `xplanung`, …) are pure re-exports of the
canonical `openbim-*` crate, pinned to its exact version, so both names share
one API and one type identity.

Road and traffic data (OKSTRA) lives in
[openbimrs/okstra](https://github.com/openbimrs/okstra).

## Development

```bash
scripts/gate.sh            # the complete gate (CI runs its sections in parallel)
scripts/gate.sh rust       # fmt, build, tests, clippy, docs, packaging
scripts/gate.sh bindings   # every npm package and wheel, built and tested
scripts/new-standard.py --help   # scaffold another standard
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for releasing.

## License

MIT. See [LICENSE](LICENSE) and [LICENSING.md](LICENSING.md). The standards
themselves remain the property of their operators; this repository contains
no schema files or specification text.
