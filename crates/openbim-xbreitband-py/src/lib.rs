//! Python binding of [`openbim_xbreitband`], published to PyPI as
//! `openbim-xbreitband` and imported as `openbim_xbreitband`. Build and test it with
//! `scripts/check-python.sh openbim-xbreitband-py`.

use pyo3::prelude::*;

/// The `openbim_xbreitband` extension module.
#[pymodule]
#[pyo3(name = "openbim_xbreitband")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xbreitband::NAME)?;
    m.add("OPERATOR", ::openbim_xbreitband::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xbreitband::HOMEPAGE)?;
    Ok(())
}
