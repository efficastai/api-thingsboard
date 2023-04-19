from app.TimeCalculation import *
import pytest


@pytest.mark.parametrize("shift_start, expected_ratio", [
    (None, 0),
    ('07:00', 50)
])
def test_get_machine_time_calculations(shift_start, expected_ratio):
    tc = TimeCalculation()
    result = tc.get_machine_time_calculations(device='test_device', shift_start=shift_start)
    assert result['api_ratio_shift_time_current_day'] == expected_ratio
