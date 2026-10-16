//! JavaScript binding of [`openbim-xrechnung`], published to npm as
//! `@openbim/xrechnung`. Build it with `scripts/build-npm-package.sh openbim-xrechnung-wasm`.

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
    openbim_xrechnung::NAME.to_owned()
}

#[cfg(test)]
mod tests {
    #[test]
    fn reports_the_canonical_standard() {
        assert_eq!(super::standard_name(), openbim_xrechnung::NAME);
        assert_eq!(super::version(), env!("CARGO_PKG_VERSION"));
    }
}
