// Runs against the built package: XSTD_NPM_PKG=<out dir> node --test ...
const assert = require("node:assert/strict");
const path = require("node:path");
const test = require("node:test");

const dir = process.env.XSTD_NPM_PKG;
if (!dir) throw new Error("set XSTD_NPM_PKG to the built package directory");
const pkg = require(path.resolve(dir));
const manifest = require(path.resolve(dir, "package.json"));

test("version matches the package manifest", () => {
  assert.equal(pkg.version(), manifest.version);
});

test("names the standard", () => {
  assert.equal(pkg.standardName(), "XBestellung");
});
