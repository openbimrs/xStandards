//! JavaScript binding of [`openbim-xbreitband`], published to npm as
//! `@openbim/xbreitband`. Build it with `scripts/build-npm-package.sh openbim-xbreitband-wasm`.

use wasm_bindgen::prelude::*;

/// The package version.
#[wasm_bindgen]
#[must_use]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_owned()
}

/// The name of the standard this package implements.
#[wasm_bindgen(js_name = standardName)]
#[must_use]
pub fn standard_name() -> String {
    openbim_xbreitband::NAME.to_owned()
}

#[cfg(test)]
mod tests {
    #[test]
    fn reports_the_canonical_standard() {
        assert_eq!(super::standard_name(), openbim_xbreitband::NAME);
        assert_eq!(super::version(), env!("CARGO_PKG_VERSION"));
    }
}
