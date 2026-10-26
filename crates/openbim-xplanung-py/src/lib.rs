//! Python binding of [`openbim_xplanung`], published to PyPI as
//! `openbim-xplanung` and imported as `openbim_xplanung`. Build and test it with
//! `scripts/check-python.sh openbim-xplanung-py`.

use pyo3::prelude::*;

/// The `openbim_xplanung` extension module.
#[pymodule]
#[pyo3(name = "openbim_xplanung")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xplanung::NAME)?;
    m.add("OPERATOR", ::openbim_xplanung::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xplanung::HOMEPAGE)?;
    Ok(())
}
