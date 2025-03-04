# Unitscalar: real-time verified dimensional analysis in Python

[![Basic validation](https://github.com/neilbalch/unitscalar/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/neilbalch/unitscalar/actions/workflows/python-package.yml)

This package implements a unit-aware number data type that keeps track of units as an inseparable part of the number. Heavily inspired by Steve Byrnes' [`numericalunits`](https://github.com/sbyrnes321/numericalunits)

- [GitHub](https://github.com/neilbalch/unitscalar)
- [PyPi](https://pypi.org/project/unitscalar)
- [TestPyPi](https://test.pypi.org/project/unitscalar)

## Valid Literals

`UnitScalar` uses [`custom-literals`](https://github.com/RocketRace/custom-literals) to hack support for custom literals into the language. These are defined for certain (arbitrary) unit strings as needed. At present:

| Literal | Unit String |       Example     |
|:-------:|-------------|-------------------|
| `x`     | `""` (N/A)  | `10 .x` or `10.x` |
| `gMM`   | `g/mol`     | `101.1.gMM`       |
| `inch`  | `in`        | `3.90.inch`       |
| `psi`   | `psi`       | `10.0.psi`        |
| `lbf`   | `lbf`       | `0.0.lbf`         |
| `K`     | `K`         | `1837.22.K`       |

As a consequence of including this feature, `unitscalar` depends on the PIP package `custom_literals`. The latter mentioned warning about stability shouldn't affect downstream projects if the literals feature is not used.

### Fair Warning

Briefly quoting the [`custom-literals` README section](https://github.com/RocketRace/custom-literals?tab=readme-ov-file#stability) on stability caveats:

> This library relies almost entirely on implementation-specific behavior of the CPython interpreter. It is not guaranteed to work on all platforms, or on all versions of Python. It has been tested on common platforms (windows, ubuntu, macos) using python 3.7 through to 3.10, but while changes that would break the library are quite unlikely, they are not impossible either.

## TODO List

- Vectorized artithmetic?
- Write example code and fill out README
