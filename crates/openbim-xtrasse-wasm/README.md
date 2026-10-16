# @openbim/xtrasse

Geodata standard for planned line routes, built on XPlanung, in JavaScript: the WebAssembly build of the
[`openbim-xtrasse`](https://crates.io/crates/openbim-xtrasse) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XTrasse documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xtrasse");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xtrasse/bundler` and
browsers without a bundler `@openbim/xtrasse/web` (call its default `init()`
first).

## License

MIT
