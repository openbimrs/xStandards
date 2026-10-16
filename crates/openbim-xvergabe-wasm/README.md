# @openbim/xvergabe

Interface standard between e-procurement platforms and bidder tools, in JavaScript: the WebAssembly build of the
[`openbim-xvergabe`](https://crates.io/crates/openbim-xvergabe) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XVergabe documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xvergabe");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xvergabe/bundler` and
browsers without a bundler `@openbim/xvergabe/web` (call its default `init()`
first).

## License

MIT
