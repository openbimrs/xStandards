//! Python binding of [`openbim_xrechnung`], published to PyPI as
//! `openbim-xrechnung` and imported as `openbim_xrechnung`. Build and test it with
//! `scripts/check-python.sh openbim-xrechnung-py`.

use pyo3::prelude::*;

/// The `openbim_xrechnung` extension module.
#[pymodule]
#[pyo3(name = "openbim_xrechnung")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xrechnung::NAME)?;
    m.add("OPERATOR", ::openbim_xrechnung::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xrechnung::HOMEPAGE)?;
    Ok(())
}
