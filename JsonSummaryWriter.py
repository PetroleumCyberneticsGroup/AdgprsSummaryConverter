import json
from AdgprsSummary import AdgprsSummary


class FieldData:
    """
    Holds all field data for the summary.
    """
    def __init__(self, summary):
        self.field = {
            'NumWells' : summary.num_wells,
            'Properties' : {
                'TIME' : summary.vec_time_steps.tolist(),
                'FGPT' : summary.vec_gas_cumulative_field.tolist(),
                'FOPT' : summary.vec_oil_cumulative_field.tolist(),
                'FWPT' : summary.vec_water_cumulative_field.tolist(),
                'FOPR' : summary.vec_gas_rates_field.tolist(),
                'FGPR' : summary.vec_oil_rates_field.tolist(),
                'FWPR' : summary.vec_water_rates_field.tolist(),
                'FGIT' : summary.vec_gas_injected_cumulative_field.tolist(),
                'FGIR' : summary.vec_gas_injected_rates_field.tolist(),
                'FOIT' : summary.vec_oil_injected_cumulative_field.tolist(),
                'FOIR' : summary.vec_oil_injected_rates_field.tolist(),
                'FWIT' : summary.vec_water_injected_cumulative_field.tolist(),
                'FWIR' : summary.vec_water_injected_rates_field.tolist()
            }
        }

    def object(self):
        return self.field

class WellData:
    """
    Holds all well data for the summary.
    Note that production and injection data are not explicitly
    separated; if the well is an injector, the rates and cumulatives
    are injected; otherwise they are produced.
    """
    def __init__(self, summary):
        self.wells = []
        for w in summary.wells:
            if w.is_injector:
                is_injector = 1
            else:
                is_injector = 0
            self.wells.append({
                'NumPerforations' : w.num_perforations,
                'IsInjector' : is_injector,
                'Properties' : {
                    'TIME' : w.vec_time_steps.tolist(),
                    'WBHP' : w.vec_bhp.tolist(),
                    'WGR' : w.vec_gas_rates.tolist(),
                    'WOR' : w.vec_oil_rates.tolist(),
                    'WWR' : w.vec_water_rates.tolist(),
                    'WGT' : w.vec_gas_cumulative.tolist(),
                    'WOT' : w.vec_oil_cumulative.tolist(),
                    'WWT' : w.vec_water_cumulative.tolist(),
                }
            })

    def object(self):
        return self.wells

class JsonSummaryWriter:
    def __init__(self, summary, output_path):
        self.field_data = FieldData(summary)
        self.well_data = WellData(summary)
        summary = {
            'Field' : self.field_data.object(),
            'Wells' : self.well_data.object()
        }
        with open(output_path, 'w') as f:
            json.dump(summary, f)
