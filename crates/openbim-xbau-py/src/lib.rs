//! Python binding of [`openbim_xbau`], published to PyPI as
//! `openbim-xbau` and imported as `openbim_xbau`. Build and test it with
//! `scripts/check-python.sh openbim-xbau-py`.

use pyo3::prelude::*;

/// The `openbim_xbau` extension module.
#[pymodule]
#[pyo3(name = "openbim_xbau")]
fn init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("STANDARD_NAME", ::openbim_xbau::NAME)?;
    m.add("OPERATOR", ::openbim_xbau::OPERATOR)?;
    m.add("HOMEPAGE", ::openbim_xbau::HOMEPAGE)?;
    Ok(())
}
