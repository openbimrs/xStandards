# @openbim/xbreitband

XBau specialist module for permits in broadband rollout and civil works (XBau-Tiefbau), in JavaScript: the WebAssembly build of the
[`openbim-xbreitband`](https://crates.io/crates/openbim-xbreitband) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XBreitband documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xbreitband");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xbreitband/bundler` and
browsers without a bundler `@openbim/xbreitband/web` (call its default `init()`
first).

## License

MIT
