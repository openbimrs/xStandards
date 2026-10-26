//! Python binding of [`openbim_xbestellung`], published to PyPI as
//! `openbim-xbestellung` and imported as `openbim_xbestellung`. Build and test it with
//! `scripts/check-python.sh openbim-xbestellung-py`.

use pyo3::prelude::*;

/// The `openbim_xbestellung` extension module.
#[pymodule]
#[pyo3(name = "openbim_xbestellung")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xbestellung::NAME)?;
    m.add("OPERATOR", ::openbim_xbestellung::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xbestellung::HOMEPAGE)?;
    Ok(())
}
