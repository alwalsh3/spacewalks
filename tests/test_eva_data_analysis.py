import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_text_to_duration_integer():
    """
    Test that text_to_duration returns expected ground truth values for typical
    durations with zero minutes
    """
    input_value = "10:00"
    assert text_to_duration(input_value) == 10


def test_text_to_duration_float1():
    """
    Test that text_to_duration returns expected ground truth values for typical
    durations with a non-zero minute component that is rational
    """
    input_value = "10:15"
    assert text_to_duration(input_value) == 10.25


def test_text_to_duration_float2():
    """
    Test that text_to_duration returns expected ground truth values for typical
    durations with a non-zero minute component that is irrational
    """
    input_value = "10:20"
    assert text_to_duration(input_value) == pytest.approx(10.33333333)

@pytest.mark.parametrize( "input_value, expected_result", [
    ("Valentina Tereshkova;", 1),
    ("Judith Resnik; Sally Ride;", 2)
])


def test_calculate_crew_size(input_value, expected_result):
    """
    Test that calculate_crew_size returns expected ground truth values for typical
    numbers of crew sizes
    """

    # Typical value
    actual_result =   calculate_crew_size(input_value)
    assert actual_result == expected_result


def test_calculate_crew_size_edge_cases():

    # Edge case 1
    actual_result = calculate_crew_size("")
    expected_result = None
    assert actual_result == expected_result