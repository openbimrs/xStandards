//! Alias for the [`openbim-xvergabe`](https://docs.rs/openbim-xvergabe) crate.
//!
//! This crate deliberately defines **nothing** of its own. It exists so
//! XVergabe is reachable under the short name practitioners actually use,
//! while there remains exactly one definition of every type.
//!
//! Adding a type here would be a defect: a dependency graph containing both
//! this crate and `openbim-xvergabe` would then hold two structurally identical
//! but distinct types, which no Cargo version resolution can unify. The
//! dependency is pinned with `=` for the same reason.
pub use openbim_xvergabe::*;
