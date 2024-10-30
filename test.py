import pandas as pd
import json
from pathlib import Path
from openff.evaluator.datasets import PhysicalProperty, PropertyPhase
from openff.evaluator.datasets.thermoml import thermoml_property
from openff.evaluator import properties
from openff.units import unit
from openff.evaluator.datasets.thermoml import ThermoMLDataSet

@thermoml_property("Osmotic coefficient", supported_phases=PropertyPhase.Liquid | PropertyPhase.Gas)
class OsmoticCoefficient(PhysicalProperty):
    """A class representation of a osmotic coeff property"""

    @classmethod
    def default_unit(cls):
        return unit.dimensionless
setattr(properties, OsmoticCoefficient.__name__, OsmoticCoefficient)

from openff.evaluator.datasets.thermoml import ThermoMLDataSet

CACHED_PROP_PATH = Path('osmotic_data.csv')

if CACHED_PROP_PATH.exists():
    prop_df = pd.read_csv(CACHED_PROP_PATH, index_col=0)
    ## delete rows with underfined thermo params to avoid pesky indexing errors
    # prop_df = prop_df.dropna(subset=['Temperature (K)'])
    # prop_df = prop_df.dropna(subset=['Pressure (kPa)'])
    data_set = ThermoMLDataSet.from_pandas(prop_df)
else:
    with open('sorted_dois.json') as f:
        doi_dat = json.load(f)
        data_set = ThermoMLDataSet.from_doi(*doi_dat['working'])

    prop_df = data_set.to_pandas()
    with CACHED_PROP_PATH.open('w') as file:
        prop_df.to_csv(CACHED_PROP_PATH)