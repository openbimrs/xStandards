//! # openbim-xtrasse
//!
//! Geodata standard for planned line routes, built on XPlanung.
//! Operated by XLeitstelle Planen und Bauen.
//! Official information: <https://xleitstelle.de/xtrassexbreitband>.
//!
//! **Status: scaffold.** This crate currently states only which standard it
//! implements. Reading, writing and validating XTrasse documents are not
//! implemented yet; nothing here encodes normative content of the standard.
//!
//! ```
//! assert_eq!(openbim_xtrasse::NAME, "XTrasse");
//! ```

/// The standard's name as its operator writes it.
pub const NAME: &str = "XTrasse";

/// The body that operates and maintains the standard.
pub const OPERATOR: &str = "XLeitstelle Planen und Bauen";

/// The operator's public page for the standard, if it has one.
pub const HOMEPAGE: Option<&str> = Some("https://xleitstelle.de/xtrassexbreitband");

/// The version of this crate (not of the standard).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
