from openff.evaluator.datasets.thermoml import ThermoMLDataSet

ds = ThermoMLDataSet.from_doi('10.1021/je800307g')
print(ds.to_pandas())