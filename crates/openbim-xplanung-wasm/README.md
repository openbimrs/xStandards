# @openbim/xplanung

Exchange standard for spatial and land-use plans (XPlanGML), in JavaScript: the WebAssembly build of the
[`openbim-xplanung`](https://crates.io/crates/openbim-xplanung) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XPlanung documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xplanung");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xplanung/bundler` and
browsers without a bundler `@openbim/xplanung/web` (call its default `init()`
first).

## License

MIT
