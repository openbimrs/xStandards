# @openbim/xbestellung

Standard for electronic purchase orders in public procurement, in JavaScript: the WebAssembly build of the
[`openbim-xbestellung`](https://crates.io/crates/openbim-xbestellung) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XBestellung documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xbestellung");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xbestellung/bundler` and
browsers without a bundler `@openbim/xbestellung/web` (call its default `init()`
first).

## License

MIT
