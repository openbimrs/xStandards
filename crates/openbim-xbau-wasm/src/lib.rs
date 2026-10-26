//! JavaScript binding of [`openbim_xbau`], published to npm as
//! `@openbim/xbau`. Build it with `scripts/build-npm-package.sh openbim-xbau-wasm`.

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
    openbim_xbau::NAME.to_owned()
}

#[cfg(test)]
mod tests {
    #[test]
    fn reports_the_canonical_standard() {
        assert_eq!(super::standard_name(), openbim_xbau::NAME);
        assert_eq!(super::version(), env!("CARGO_PKG_VERSION"));
    }
}
