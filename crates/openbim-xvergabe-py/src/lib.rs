//! Python binding of [`openbim-xvergabe`], published to PyPI as
//! `openbim-xvergabe` and imported as `openbim_xvergabe`. Build and test it with
//! `scripts/check-python.sh openbim-xvergabe-py`.

use pyo3::prelude::*;

/// The `openbim_xvergabe` extension module.
#[pymodule]
#[pyo3(name = "openbim_xvergabe")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xvergabe::NAME)?;
    m.add("OPERATOR", ::openbim_xvergabe::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xvergabe::HOMEPAGE)?;
    Ok(())
}
