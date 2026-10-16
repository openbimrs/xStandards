# openbim-xrechnung

German CIUS of the EN 16931 electronic invoice, in Python: bindings for the
[`openbim-xrechnung`](https://crates.io/crates/openbim-xrechnung) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XRechnung documents are not implemented yet.

```python
import openbim_xrechnung
print(openbim_xrechnung.STANDARD_NAME, openbim_xrechnung.__version__)
```

## License

MIT
