import h5py
import numpy as np


def accumulate(vec_time, vec_prop):
    dtime = np.diff(vec_time)
    cumulative = np.cumsum(dtime*vec_prop[:-1])
    return np.insert(cumulative, 0, 0.0)


class Perforation:
    """ This class holds all vectors for one perforation """
    def __init__(self, times, pressures, grat, orat, wrat, temp, dens):
        self.vec_time_steps = times
        self.vec_pressures = pressures
        self.vec_gas_rates = grat
        self.vec_gas_cumulative = accumulate(self.vec_time_steps, self.vec_gas_rates)
        self.vec_oil_rates = orat
        self.vec_oil_cumulative = accumulate(self.vec_time_steps, self.vec_oil_rates)
        self.vec_water_rates = wrat
        self.vec_water_cumulative = accumulate(self.vec_time_steps, self.vec_water_rates)
        self.vec_temperatures = temp
        self.vec_average_densities = dens


class Well:
    """ This class is used to hold/access the data for a single well in an ADGPRS summary. """
    def __init__(self, single_well_states, vec_time_steps):
        self._well_states = single_well_states
        self._phase_rates = single_well_states['vPhaseRates']
        self._phase_rates_sc = single_well_states['vPhaseRatesAtSC']
        self.num_perforations = len(single_well_states['vTemperatures'][0])
        self.vec_bhp = np.array([p[0] for p in self._well_states['vPressures']])
        self.vec_time_steps = vec_time_steps
        self.vec_gas_rates_at_sc = np.array([p[0] for p in self._phase_rates_sc])
        self.vec_gas_cumulative_at_sc = accumulate(self.vec_time_steps, self.vec_gas_rates_at_sc)
        self.vec_oil_rates_at_sc = np.array([p[1] for p in self._phase_rates_sc])
        self.vec_oil_cumulative_at_sc = accumulate(self.vec_time_steps, self.vec_oil_rates_at_sc)
        self.vec_water_rates_at_sc = np.array([p[2] for p in self._phase_rates_sc])
        self.vec_water_cumulative_at_sc = accumulate(self.vec_time_steps, self.vec_water_rates_at_sc)
        self.perforations = []
        for p in range(self.num_perforations):
            p_grat = np.array([phr[p*3+0] for phr in self._phase_rates])
            p_orat = np.array([phr[p*3+1] for phr in self._phase_rates])
            p_wrat = np.array([phr[p*3+2] for phr in self._phase_rates])
            p_pres = np.array([pr[p+1] for pr in self._well_states['vPressures']])
            p_temp = np.array([t[p] for t in self._well_states['vTemperatures']])
            p_dens = np.array([d[p] for d in self._well_states['vAverageDensity']])
            self.perforations.append(Perforation(self.vec_time_steps, p_pres, p_grat, p_orat, p_wrat, p_temp, p_dens))

    @property
    def vec_gas_rates(self):
        well_rate = np.zeros(self.perforations[0].vec_gas_rates.shape)
        for p in self.perforations:
            well_rate += p.vec_gas_rates
        return well_rate

    @property
    def vec_oil_rates(self):
        well_rate = np.zeros(self.perforations[0].vec_oil_rates.shape)
        for p in self.perforations:
            well_rate += p.vec_oil_rates
        return well_rate

    @property
    def vec_water_rates(self):
        well_rate = np.zeros(self.perforations[0].vec_water_rates.shape)
        for p in self.perforations:
            well_rate += p.vec_water_rates
        return well_rate

    @property
    def vec_gas_cumulative(self):
        cumulative = np.zeros(self.perforations[0].vec_gas_cumulative.shape)
        for p in self.perforations:
            cumulative += p.vec_gas_cumulative
        return cumulative

    @property
    def vec_oil_cumulative(self):
        cumulative = np.zeros(self.perforations[0].vec_oil_cumulative.shape)
        for p in self.perforations:
            cumulative += p.vec_oil_cumulative
        return cumulative

    @property
    def vec_water_cumulative(self):
        cumulative = np.zeros(self.perforations[0].vec_water_cumulative.shape)
        for p in self.perforations:
            cumulative += p.vec_water_cumulative
        return cumulative

    @property
    def is_injector(self):
        return self.vec_water_cumulative[-1] < -1.0 or self.vec_gas_cumulative[-1] < -1

class AdgprsSummary:
    """ This class represents a single ADGPRS summary. """

    def __init__(self, summary_path):
        self.summary_path = summary_path
        self.h5file = h5py.File(summary_path, 'r')
        self.h5gr_restart = self.h5file['RESTART']
        self.h5gr_flow_transport = self.h5file['FLOW_TRANSPORT']
        self.h5ds_well_states = self.h5gr_flow_transport['WELL_STATES']
        self.num_wells = self.h5ds_well_states.shape[0]
        self.vec_time_steps = self.h5gr_restart['TIMES'][:]  # 1D vector
        self.wells = []
        for w in range(self.num_wells):
            self.wells.append(Well(self.h5ds_well_states[w], self.vec_time_steps))

    @property
    def vec_gas_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_gas_rates.shape)
        for w in self.wells:
            if not w.is_injector:
                field_rate += w.vec_gas_rates
        return field_rate

    @property
    def vec_oil_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_oil_rates.shape)
        for w in self.wells:
            if not w.is_injector:
                field_rate += w.vec_oil_rates
        return field_rate

    @property
    def vec_water_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_water_rates.shape)
        for w in self.wells:
            if not w.is_injector:
                field_rate += w.vec_water_rates
        return field_rate

    @property
    def vec_gas_injected_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_gas_rates.shape)
        for w in self.wells:
            if w.is_injector:
                field_rate += w.vec_gas_rates
        return field_rate

    @property
    def vec_oil_injected_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_oil_rates.shape)
        for w in self.wells:
            if w.is_injector:
                field_rate += w.vec_oil_rates
        return field_rate

    @property
    def vec_water_injected_rates_field(self):
        field_rate = np.zeros(self.wells[0].vec_water_rates.shape)
        for w in self.wells:
            if w.is_injector:
                field_rate += w.vec_water_rates
        return field_rate

    @property
    def vec_gas_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_gas_cumulative.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_gas_cumulative
        return cumulative

    @property
    def vec_oil_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_oil_cumulative.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_oil_cumulative
        return cumulative

    @property
    def vec_water_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_water_cumulative.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_water_cumulative
        return cumulative

    @property
    def vec_gas_cumulative_at_sc_field(self):
        cumulative = np.zeros(self.wells[0].vec_gas_cumulative_at_sc.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_gas_cumulative_at_sc
        return cumulative

    @property
    def vec_oil_cumulative_at_sc_field(self):
        cumulative = np.zeros(self.wells[0].vec_oil_cumulative_at_sc.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_oil_cumulative_at_sc
        return cumulative

    @property
    def vec_water_cumulative_at_sc_field(self):
        cumulative = np.zeros(self.wells[0].vec_water_cumulative_at_sc.shape)
        for w in self.wells:
            if not w.is_injector:
                cumulative += w.vec_water_cumulative_at_sc
        return cumulative


    @property
    def vec_gas_injected_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_gas_cumulative.shape)
        for w in self.wells:
            if w.is_injector:
                cumulative += w.vec_gas_cumulative
        return cumulative

    @property
    def vec_oil_injected_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_oil_cumulative.shape)
        for w in self.wells:
            if w.is_injector:
                cumulative += w.vec_oil_cumulative
        return cumulative

    @property
    def vec_water_injected_cumulative_field(self):
        cumulative = np.zeros(self.wells[0].vec_water_cumulative.shape)
        for w in self.wells:
            if w.is_injector:
                cumulative += w.vec_water_cumulative
        return cumulative

#
# summary = AdgprsSummary("/home/einar/Documents/GitHub/PCG/FieldOpt/examples/ADGPRS/5spot/5SPOT.SIM.H5")
#
# print('Num wells: ', len(summary.wells))
# wc = 0
# for w in summary.wells:
#     print('WELL ', wc)
#     print('is injector: ', w.is_injector)
#     print('num perf: ', w.num_perforations)
#     print('bhp0: ', w.vec_bhp[0])
#     print(w.perforations[0].vec_average_densities)
#     print(w.perforations[0].vec_gas_cumulative)
#     print(w.vec_gas_cumulative)
#     print(w.vec_water_cumulative)
#     wc += 1
#
# print(summary.vec_oil_cumulative_field)
