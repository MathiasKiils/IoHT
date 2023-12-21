import time
import board
import busio
import displayio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
import terminalio
import wifi
import socketpool
import adafruit_requests
from time import sleep
from c02_ppm import measure_co2_concentration
from dht11 import read_dht_sensor

# Constants
BLACK = 0x000000
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 160
DISPLAY_ROTATION = 90
TEXT_COLOR = 0xFFFFFF
REFRESH_DELAY = 10  # seconds

# Pin configuration
spi_pins = {"mosi": board.GP19, "clock": board.GP18}
display_pins = {"reset": board.GP20, "cs": board.GP22, "dc": board.GP21}

# Release any existing displays
displayio.release_displays()

# SPI and Display setup
spi = busio.SPI(clock=spi_pins["clock"], MOSI=spi_pins["mosi"])
display_bus = displayio.FourWire(spi, command=display_pins["dc"], chip_select=display_pins["cs"], reset=display_pins["reset"])
display = ST7735R(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, bgr=True)
display.rotation = DISPLAY_ROTATION

# Display Group setup
splash = displayio.Group()
display.show(splash)

# Background setup
color_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BLACK
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
splash.append(bg_sprite)

# Text area for sensor data
text_group = displayio.Group(scale=1, x=11, y=24)
text_area = label.Label(terminalio.FONT, text="", color=TEXT_COLOR)
text_group.append(text_area)
splash.append(text_group)

# Wi-Fi Credentials
SSID = "LTE-1840"
PASSWORD = "12345678"

# Connect to Wi-Fi
wifi.radio.connect(SSID, PASSWORD)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context=None)

# Flask Server URL
server_url = 'http://192.168.0.101:5000/device1_POST'  # Replace with your Flask server address

time.sleep(30)  # Wait for 30 seconds before starting the main loop

# Main loop
while True:
    co2_concentration, co2_category = measure_co2_concentration()
    temperature, humidity = read_dht_sensor()
    sensor_data = {
        "co2_concentration": co2_concentration,
        "co2_category": co2_category,
        "temperature": temperature,
        "humidity": humidity
    }

    # Send data to Flask server
    try:
        print(f"CO2: {co2_concentration} ppm {co2_category}\nTemp: {temperature:.1f}°C\nHumidity: {humidity:.1f}%")
        response = requests.post(server_url, json=sensor_data)
        print("Data sent:", sensor_data, "| Response:", response.text)
    except Exception as e:
        print("Failed to send data:", e)

    # Update display
    display_text = f"CO2: {co2_concentration} ppm {co2_category}\nTemp: {temperature:.1f}°C\nHumidity: {humidity:.1f}%"
    text_area.text = display_text

    sleep(REFRESH_DELAY)
