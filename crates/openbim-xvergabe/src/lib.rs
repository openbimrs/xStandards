//! # openbim-xvergabe
//!
//! Interface standard between e-procurement platforms and bidder tools.
//! Operated by IT-Planungsrat.
//!
//! **Status: scaffold.** This crate currently states only which standard it
//! implements. Reading, writing and validating XVergabe documents are not
//! implemented yet; nothing here encodes normative content of the standard.
//!
//! ```
//! assert_eq!(openbim_xvergabe::NAME, "XVergabe");
//! ```

/// The standard's name as its operator writes it.
pub const NAME: &str = "XVergabe";

/// The body that operates and maintains the standard.
pub const OPERATOR: &str = "IT-Planungsrat";

/// The operator's public page for the standard, if it has one.
pub const HOMEPAGE: Option<&str> = None;

/// The version of this crate (not of the standard).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
