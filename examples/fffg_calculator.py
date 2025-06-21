from unitscalar import UnitScalar as us
from periodictable import formulas as fm
import math
import numpy as np


# Implement hashing for the periodictable.formulas.Formula class type
def formula_hash(fmla: fm.Formula):
    return hash(tuple(fmla.__dict__.values()))


# https://stackoverflow.com/a/4719108/3339274
fm.Formula.__hash__ = formula_hash  # type: ignore

################################################################################
#                           Define FFFg Molar Mass
################################################################################

USE_CUSTOM_MIX = True
# https://periodictable.readthedocs.io/en/latest/api/formulas.html#periodictable.formulas.Formula.mass
RECIPES: dict[str, dict[fm.Formula, float]] = {
    # Reference for usual black powder mix: https://chem.libretexts.org/Bookshelves/General_Chemistry/ChemPRIME_(Moore_et_al.)/03%3A_Using_Chemical_Equations_in_Calculations/3.03%3A_The_Limiting_Reagent/3.3.06%3A_Forensics-_Gunpowder_Stoichiometry
    "FFFg": {
        fm.formula("KNO3"): 0.75,  # type: ignore
        fm.formula("S"): 0.10,  # type: ignore
        fm.formula("C"): 0.15,  # type: ignore
    },
    # https://en.wikipedia.org/wiki/Black_powder_substitute#Types
    "Pyrodex": {
        fm.formula("KNO3"): 0.45,  # type: ignore
        # Simplification of charcoal
        fm.formula("C"): 0.09,  # type: ignore
        fm.formula("S"): 0.06,  # type: ignore
        fm.formula("KClO4"): 0.19,  # type: ignore
        fm.formula("C7H5NaO2"): 0.11,  # type: ignore
        fm.formula("C2H4N4"): 0.06,  # type: ignore
        # Assuming only one monomer in chain
        fm.formula("C6H10O5"): 0.04,  # type: ignore
    },
}
COMPONENT_RATIO =  RECIPES["FFFg"]

global FFFg_molar_mass
if USE_CUSTOM_MIX:
    assert np.isclose(
        np.sum(list(COMPONENT_RATIO.values())), 1
    ), f"Sum of ratios is not 1 (100%), instead is {np.sum(list(COMPONENT_RATIO.values()))}"
    pyro_molar_mass = 0
    for component, ratio in COMPONENT_RATIO.items():
        pyro_molar_mass += component.mass.gMM * ratio
else:
    # Calculated based on ratio of g predicted using mixed-unit equation (http://hararocketry.org/hara/resources/how-to-size-ejection-charge) and mol predicted using SI-unit ideal gas law
    pyro_molar_mass = (69.78).gMM

print(f"Pyro molar mass is: {pyro_molar_mass:0.2f;g/mol}")

################################################################################
#                     Calculate Required FFFg Quantity
################################################################################

# Design parameters
CHAMBER_ID = (3.90).inch  # Chamber Internal Diameter
CHAMBER_LENGTH = (10.0).inch  # Chamber Length
# Desired pop pressure (negating positive retention)
POP_PRESSURE = (10.0).psi
# Force required to break positive retention (e.g. shear bolts)
# - https://web.archive.org/web/20131026023457/http://www.rocketmaterials.org/datastore/cord/Shear_Pins/index.php
# - http://feretich.com/Rocketry/Resources/shearPins.html
SHEAR_FORCE = (0.0).lbf

# Assumed quantities
# http://hararocketry.org/hara/resources/how-to-size-ejection-charge
FFFg_combustion_temp = (1837.22).K
Rgas = us.UnitScalar(8.31446261815324, "J/K mol")

bulkhead_area = math.pi * (CHAMBER_ID / 2) ** 2
bulkhead_force = POP_PRESSURE * SHEAR_FORCE
chamber_volume = bulkhead_area * CHAMBER_LENGTH

# Based on the following mixed-unit formula: http://hararocketry.org/hara/resources/how-to-size-ejection-charge
pyro_mass = (
    pyro_molar_mass
    * (POP_PRESSURE + SHEAR_FORCE / bulkhead_area)
    * chamber_volume
    / (Rgas * FFFg_combustion_temp)
)

# print("Pyro Mass:", round(float(pyro_mass) * 1000, 2), "g", sep=" ")
# print(f"Pyro Mass: {pyro_mass.to_units("g"):.2f} g")
print(f"Pyro Mass: {pyro_mass:0.2f;g}")
