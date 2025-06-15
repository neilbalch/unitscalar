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

global FFFg_molar_mass
if USE_CUSTOM_MIX:
    # Reference for usual black powder mix: https://chem.libretexts.org/Bookshelves/General_Chemistry/ChemPRIME_(Moore_et_al.)/03%3A_Using_Chemical_Equations_in_Calculations/3.03%3A_The_Limiting_Reagent/3.3.06%3A_Forensics-_Gunpowder_Stoichiometry
    # https://periodictable.readthedocs.io/en/latest/api/formulas.html#periodictable.formulas.Formula.mass
    COMPONENT_RATIO = {
        fm.formula("KNO3"): 0.75,  # type: ignore
        fm.formula("S"): 0.10,  # type: ignore
        fm.formula("C"): 0.15,  # type: ignore
    }

    assert np.sum(list(COMPONENT_RATIO.values())) == 1, "Sum of ratios is not 1 (100%)"
    FFFg_molar_mass = 0
    for component, ratio in COMPONENT_RATIO.items():
        FFFg_molar_mass += component.mass.gMM * ratio
else:
    # Calculated based on ratio of g predicted using mixed-unit equation (http://hararocketry.org/hara/resources/how-to-size-ejection-charge) and mol predicted using SI-unit ideal gas law
    FFFg_molar_mass = (69.78).gMM

print(f"FFFg Molar Mass is: {FFFg_molar_mass.fmt_in_units('g/mol', 2)}")

################################################################################
#                     Calculate Required FFFg Quantity
################################################################################

# Design parameters
chamber_id = (3.90).inch  # Chamber Internal Diameter
chamber_length = (10.0).inch  # Chamber Length
# Desired pop pressure (negating positive retention)
pop_pressure = (10.0).psi
# Force required to break positive retention (e.g. shear bolts)
# - https://web.archive.org/web/20131026023457/http://www.rocketmaterials.org/datastore/cord/Shear_Pins/index.php
# - http://feretich.com/Rocketry/Resources/shearPins.html
shear_force = (0.0).lbf

# Assumed quantities
# http://hararocketry.org/hara/resources/how-to-size-ejection-charge
FFFg_combustion_temp = (1837.22).K
Rgas = us.UnitScalar(8.31446261815324, "J/K mol")

bulkhead_area = math.pi * (chamber_id / 2) ** 2
bulkhead_force = pop_pressure * shear_force
chamber_volume = bulkhead_area * chamber_length

# Based on the following mixed-unit formula: http://hararocketry.org/hara/resources/how-to-size-ejection-charge
FFFg_mass = (
    FFFg_molar_mass
    * (pop_pressure + shear_force / bulkhead_area)
    * chamber_volume
    / (Rgas * FFFg_combustion_temp)
)

# print("FFFg Mass:", round(float(FFFg_mass) * 1000, 2), "g", sep=" ")
# print(f"FFFg Mass: {FFFg_mass.to_units("g"):.2f} g")
print(f"FFFg Mass: {FFFg_mass.fmt_in_units('g', 2)}")
