# read version from installed package
from importlib.metadata import version
__version__ = version("weather_jz4169")

from .weather_jz4169 import (celsius_to_fahrenheit, summarize_temperatures, clean_readings)