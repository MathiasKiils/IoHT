import board
import adafruit_dht
import time

def read_dht_sensor():
    dht_pin = board.GP28
    dht_sensor = adafruit_dht.DHT11(dht_pin)

    try:
        humidity = dht_sensor.humidity
        temperature = dht_sensor.temperature
        return temperature, humidity

    except Exception as e:
        print("Error reading DHT sensor:", e)
        return None, None

    finally:
        dht_sensor.exit()

# Uncomment below line to test the function directly
# print(read_dht_sensor())