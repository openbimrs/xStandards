# openbim-xbestellung

Standard for electronic purchase orders in public procurement, in Python: bindings for the
[`openbim-xbestellung`](https://crates.io/crates/openbim-xbestellung) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XBestellung documents are not implemented yet.

```python
import openbim_xbestellung
print(openbim_xbestellung.STANDARD_NAME, openbim_xbestellung.__version__)
```

## License

MIT
