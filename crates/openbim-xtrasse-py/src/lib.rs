//! Python binding of [`openbim_xtrasse`], published to PyPI as
//! `openbim-xtrasse` and imported as `openbim_xtrasse`. Build and test it with
//! `scripts/check-python.sh openbim-xtrasse-py`.

use pyo3::prelude::*;

/// The `openbim_xtrasse` extension module.
#[pymodule]
#[pyo3(name = "openbim_xtrasse")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xtrasse::NAME)?;
    m.add("OPERATOR", ::openbim_xtrasse::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xtrasse::HOMEPAGE)?;
    Ok(())
}
