# openbim-xvergabe

Interface standard between e-procurement platforms and bidder tools, in Python: bindings for the
[`openbim-xvergabe`](https://crates.io/crates/openbim-xvergabe) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XVergabe documents are not implemented yet.

```python
import openbim_xvergabe
print(openbim_xvergabe.STANDARD_NAME, openbim_xvergabe.__version__)
```

## License

MIT
