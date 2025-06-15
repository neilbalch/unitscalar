# Unitscalar: real-time verified dimensional analysis in Python

[![Basic validation](https://github.com/neilbalch/unitscalar/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/neilbalch/unitscalar/actions/workflows/python-package.yml)

This package implements a unit-aware number data type that keeps track of units as an inseparable part of the number. Arithmetic operations strongly protect against inadvertently combining incompatible units. Heavily inspired by Steve Byrnes' [`numericalunits`](https://github.com/sbyrnes321/numericalunits)

- [GitHub](https://github.com/neilbalch/unitscalar)
- [PyPi](https://pypi.org/project/unitscalar)
- [TestPyPi](https://test.pypi.org/project/unitscalar)

## Implemented Features

- Instantiate with a floating-point number and a string representing a unit (*e.g. `"kg mm / ms2"`*)
  - Most common SI units and some imperial/customary are supported
  - SI unit prefixes from femto to tera
    - `hPa` is implemented specifically because the hecto prefix is not used very often

  ```python
  >>> from unitscalar import UnitScalar as us
  >>> list(us.UnitScalar.VALID_UNITS.keys())
  ['m', 's', 'kg', 'C', 'K', 'in', 'L', 'Hz', 'rpm', 'g', 'lbm', 'J', 'Wh', 'mol', 'N', 'lbf', 'Pa', 'hPa', 'bar', 'atm', 'psi', 'W', 'Ah', 'A', 'V', 'ohm', 'T', 'F', 'H']
  >>> list(us.UnitScalar.VALID_PREFIXES.keys())
  ['f', 'p', 'n', 'u', 'm', 'k', 'M', 'G', 'T']
  >>>
  ```

- Format as a string
- Get raw floating point number
- Get raw integer number (*truncated*)
- Compare units with another `UnitScalar` object, or a unit string
- Get raw floating point number in other (*equivalent*) units
- Format as a string in other (*equivalent*) units
- Fundamental algebraic operations (*operands can be `UnitScalar` or integral types*)
  - Add / subtract
  - Multiply / divide
  - Raise to power (*frational powers allowed*)
- Instantiate with custom literals (*see below*)

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
