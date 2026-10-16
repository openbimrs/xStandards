//! # openbim-xbestellung
//!
//! Standard for electronic purchase orders in public procurement.
//! Operated by Koordinierungsstelle für IT-Standards (KoSIT).
//! Official information: <https://xeinkauf.de/xbestellung/>.
//!
//! **Status: scaffold.** This crate currently states only which standard it
//! implements. Reading, writing and validating XBestellung documents are not
//! implemented yet; nothing here encodes normative content of the standard.
//!
//! ```
//! assert_eq!(openbim_xbestellung::NAME, "XBestellung");
//! ```

/// The standard's name as its operator writes it.
pub const NAME: &str = "XBestellung";

/// The body that operates and maintains the standard.
pub const OPERATOR: &str = "Koordinierungsstelle für IT-Standards (KoSIT)";

/// The operator's public page for the standard, if it has one.
pub const HOMEPAGE: Option<&str> = Some("https://xeinkauf.de/xbestellung/");

/// The version of this crate (not of the standard).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
