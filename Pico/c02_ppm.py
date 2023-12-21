import time
import board
from analogio import AnalogIn

def measure_co2_concentration():
    analog_pin = AnalogIn(board.GP27)

    good_threshold = 400
    medium_threshold = 1000

    try:
        raw_value = analog_pin.value
        voltage = (raw_value / 4095.0) * 3.3
        co2_ppm = voltage * 50
        co2_ppm_int = int(co2_ppm)

        if co2_ppm_int < good_threshold:
            category = "^_^"
        elif co2_ppm_int < medium_threshold:
            category = "-_-"
        else:
            category = "x_x"

        return co2_ppm_int, category

    finally:
        analog_pin.deinit()

# Uncomment below line to test the function directly
# print(measure_co2_concentration())