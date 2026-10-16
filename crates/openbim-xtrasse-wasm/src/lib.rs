//! JavaScript binding of [`openbim-xtrasse`], published to npm as
//! `@openbim/xtrasse`. Build it with `scripts/build-npm-package.sh openbim-xtrasse-wasm`.

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
    openbim_xtrasse::NAME.to_owned()
}

#[cfg(test)]
mod tests {
    #[test]
    fn reports_the_canonical_standard() {
        assert_eq!(super::standard_name(), openbim_xtrasse::NAME);
        assert_eq!(super::version(), env!("CARGO_PKG_VERSION"));
    }
}
