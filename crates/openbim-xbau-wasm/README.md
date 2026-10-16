# @openbim/xbau

XÖV message standard for building-permit procedures, including the XBau core module, in JavaScript: the WebAssembly build of the
[`openbim-xbau`](https://crates.io/crates/openbim-xbau) Rust crate.

**Status: scaffold.** The package states which standard it implements;
reading, writing and validating XBau documents are not implemented yet.

```js
const { standardName, version } = require("@openbim/xbau");
console.log(standardName(), version());
```

Node uses the CommonJS build; bundlers get `@openbim/xbau/bundler` and
browsers without a bundler `@openbim/xbau/web` (call its default `init()`
first).

## License

MIT
