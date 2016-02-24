import csv
import numpy as np

class FieldData:
    """
    Holds all field data for the summary.
    """

    def __init__(self, summary):
        self.headers = ['TIME',
                        'FGPT', 'FOPT', 'FWPT',
                        'FOPR', 'FGPR', 'FWPR',
                        'FGIT', 'FGIR', 'FOIT',
                        'FOIR', 'FWIT', 'FWIR']
        self.data = np.zeros([summary.vec_time_steps.shape[0], len(self.headers)])
        self.data[:, 0 ] = summary.vec_time_steps.tolist()
        self.data[:, 1 ] = summary.vec_gas_cumulative_field.tolist()
        self.data[:, 2 ] = summary.vec_oil_cumulative_field.tolist()
        self.data[:, 3 ] = summary.vec_water_cumulative_field.tolist()
        self.data[:, 4 ] = summary.vec_gas_rates_field.tolist()
        self.data[:, 5 ] = summary.vec_oil_rates_field.tolist()
        self.data[:, 6 ] = summary.vec_water_rates_field.tolist()
        self.data[:, 7 ] = summary.vec_gas_injected_cumulative_field.tolist()
        self.data[:, 8 ] = summary.vec_gas_injected_rates_field.tolist()
        self.data[:, 9 ] = summary.vec_oil_injected_cumulative_field.tolist()
        self.data[:, 10] = summary.vec_oil_injected_rates_field.tolist()
        self.data[:, 11] = summary.vec_water_injected_cumulative_field.tolist()
        self.data[:, 12] = summary.vec_water_injected_rates_field.tolist()


class WellData:
    """
    Holds all well data for the summary.
    Note that production and injection data are not explicitly
    separated; if the well is an injector, the rates and cumulatives
    are injected; otherwise they are produced.
    """

    def __init__(self, summary):
        self.headers = []
        self.header_base = ['WBHP', 'WGR', 'WOR', 'WWR', 'WGT', 'WOT', 'WWT']
        self.data = np.zeros([summary.vec_time_steps.shape[0], len(self.header_base)*summary.num_wells])
        windex = 0
        for w in summary.wells:
            self.headers += [h+str(windex) for h in self.header_base]
            self.data[:, windex*len(self.header_base)+0] = w.vec_bhp.tolist()
            self.data[:, windex*len(self.header_base)+1] = w.vec_gas_rates.tolist()
            self.data[:, windex*len(self.header_base)+2] = w.vec_oil_rates.tolist()
            self.data[:, windex*len(self.header_base)+3] = w.vec_water_rates.tolist()
            self.data[:, windex*len(self.header_base)+4] = w.vec_gas_cumulative.tolist()
            self.data[:, windex*len(self.header_base)+5] = w.vec_oil_cumulative.tolist()
            self.data[:, windex*len(self.header_base)+6] = w.vec_water_cumulative.tolist()
            windex += 1


class CsvSummaryWriter:
    """
    Main class. Initializes the data classes and writes the CSV file.
    """

    def __init__(self, summary, output_path):
        self.field_data = FieldData(summary)
        self.well_data = WellData(summary)

        # Write the csv file
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.field_data.headers + self.well_data.headers)
            for row in range(self.field_data.data.shape[0]):
                writer.writerow(self.field_data.data[row, :].tolist() + self.well_data.data[row, :].tolist())
