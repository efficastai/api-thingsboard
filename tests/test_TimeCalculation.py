from app.TimeCalculation import *


def test_calculate_time_values():
    tc = TimeCalculation()
    pya_tuple = [(0, 100), (1, 200), (1, 300), (0, 400), (0, 500)]
    expected_output = (200, 400)
    assert tc.calculate_time_values(pya_tuple) == expected_output
