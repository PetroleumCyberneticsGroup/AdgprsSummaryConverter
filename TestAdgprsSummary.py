import pytest
import numpy as np
from AdgprsSummary import AdgprsSummary
from AdgprsSummary import accumulate
"""
This module contains unit tests for the ADGPRS summary reader.
The tests are written using the pytest framewort, and should be
run by executing `python3 -m pytest -v TestAdgprsSummary.py`
"""

summary = AdgprsSummary("../../examples/ADGPRS/5spot/5SPOT.SIM.H5")

expected_time_vector = np.array([0., 3., 18., 48., 50., 65., 95., 100.])
expected_field_oil_rates = np.array([7618.01495079, 3209.43370259,
                                     3793.45498694, 3504.66944551,
                                     3485.50337263, 3339.91339197,
                                     3035.24303151, 2985.08344798])


class TestGeneral:
    def test_num_wells(self):
        assert summary.num_wells == 5

    def test_time_steps(self):
        assert len(summary.vec_time_steps) == 8
        assert np.array_equal(summary.vec_time_steps, expected_time_vector)

    def test_accumulate_function(self):
        assert sorted(accumulate([0, 1, 3, 6], [1000, 100, 10, 1])) == sorted([0., 1000., 1200., 1230.])


class TestFieldProps:
    def test_field_oil_rates(self):
        assert np.allclose(summary.vec_oil_rates_field, expected_field_oil_rates)
    # Missing:
    #   Water and gas production rates
    #   Production cumulatives
    #   Injection rates
    #   Injection cumulatives
    #   Everything at both surface and reservoir level


class TestWellProps:
    pass
    # Missing:
    #   All production rates
    #   Production cumulatives
    #   Injector/producer
    #   Injection rates
    #   Injection cumulatives
    #   Everything at both surface and reservoir level
    #   Number of perforations
    #   BHP


class TestPerforationProps:
    pass
    # Missing:
    #   Pressures
    #   All rates
    #   All cumulatives
    #   Temperatures
    #   Average densities
