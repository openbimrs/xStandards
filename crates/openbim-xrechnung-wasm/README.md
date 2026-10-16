# @openbim/xrechnung

German CIUS of the EN 16931 electronic invoice, in JavaScript: the WebAssembly build of the
[`openbim-xrechnung`](https://crates.io/crates/openbim-xrechnung) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XRechnung documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xrechnung");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xrechnung/bundler` and
browsers without a bundler `@openbim/xrechnung/web` (call its default `init()`
first).

## License

MIT
