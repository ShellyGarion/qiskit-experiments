# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Class to test the backend calibrations."""

import qiskit.pulse as pulse
from qiskit.test import QiskitTestCase
from qiskit.test.mock import FakeArmonk

from qiskit_experiments.calibration_management import BackendCalibrations
from qiskit_experiments.calibration_management.basis_gate_library import FixedFrequencyTransmon


class TestBackendCalibrations(QiskitTestCase):
    """Class to test the functionality of a BackendCalibrations"""

    def test_run_options(self):
        """Test that we can get run options."""
        cals = BackendCalibrations(FakeArmonk())

        self.assertEqual(cals.get_meas_frequencies(), [6993370669.000001])
        self.assertEqual(cals.get_qubit_frequencies(), [4971852852.405576])

    def test_setup_withLibrary(self):
        """Test that we can setup with a library."""

        cals = BackendCalibrations(
            FakeArmonk(),
            library=FixedFrequencyTransmon(
                basis_gates=["x", "sx"], default_values={"duration": 320}
            ),
        )

        # Check the x gate
        with pulse.build(name="x") as expected:
            pulse.play(pulse.Drag(duration=320, amp=0.5, sigma=80, beta=0), pulse.DriveChannel(0))

        self.assertEqual(cals.get_schedule("x", (0,)), expected)

        # Check the sx gate
        with pulse.build(name="sx") as expected:
            pulse.play(pulse.Drag(duration=320, amp=0.25, sigma=80, beta=0), pulse.DriveChannel(0))

        self.assertEqual(cals.get_schedule("sx", (0,)), expected)
