import weather_jz4169
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_jz4169 import (celsius_to_fahrenheit, summarize_temperatures, clean_readings)

def test_version_is_defined():
    assert isinstance(weather_jz4169.__version__, str)


# Check whether Celsius temperatures are correctly converted to Fahrenheit temperatures
@pytest.mark.parametrize("celsius, expected",
                         [(0, 32), (100, 212), (-40, -40), (37, 98.6), (-273.15, -459.67)])
def test_celsius_to_fahrenheit(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


# Check whether invalid temperatures produce the expected error output
@pytest.mark.parametrize("bad_input, expected_error",
                         [("flower", TypeError), (None, TypeError), ("12", TypeError), (-280, ValueError)])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


# Check whether the missing value is ignored when calculating the mean, minimum, and maximum values for temperatures
def test_summarize_temperatures():
    # Arrange
    temperatures = [20.0, float("nan"), 40.0]
    # Act
    results = summarize_temperatures(temperatures)
    # Assert
    assert results["mean"] == 30.0
    assert results["min"] == 20.0
    assert results["max"] == 40.0
    assert results["n_missing"] == 1


# Create a DataFrame that contains sample temperature data
@pytest.fixture
def raw_readings():
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],})


# Check whether the fixture has the correct columns, number of rows, and number of missing temperature values
def test_raw_readings_fixture(raw_readings):
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1


# Check whether the cleaned data matches the expected results built by hand
def test_clean_readings(raw_readings):
    cleaned_data = clean_readings(raw_readings)
    expected_results = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4]})
    assert_frame_equal(cleaned_data, expected_results)
