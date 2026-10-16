# xplanung

Short-name package for XPlanung.

This crate is a **pure re-export** of
[`openbim-xplanung`](https://crates.io/crates/openbim-xplanung). It defines nothing of
its own, so both package names expose one canonical API and one type identity.
The dependency is pinned to the exact canonical version.

```toml
xplanung = "0.1"
# equivalent API to:
openbim-xplanung = "0.1"
```

## License

MIT
