from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import time
from time import sleep
import requests

app = Flask(__name__)

# # Wi-Fi Credentials
# SSID = "catch"
# PASSWORD = "12345678"

# Connect to Wi-Fi
# wifi.radio.connect(SSID, PASSWORD)
# pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl_context=None)

# Flask Server URL
server_url = 'http://192.168.1.4:5000/device1_POST'

# Set up SQLite database and tables
conn = sqlite3.connect('Picodata.db')
cursor = conn.cursor()

# Define tables and schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS device1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        temp INTEGER,
        co2 INTEGER,
        fugt INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS device2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        temp INTEGER,
        co2 INTEGER,
        fugt INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS device3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        temp INTEGER,
        co2 INTEGER,
        fugt INTEGER
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()


def collect_and_insert_random_data(device_id):
    data = request.json

    # Using the 'with' statement for automatic connection closing
    with sqlite3.connect('Picodata.db') as conn:
        cursor = conn.cursor()

        # Insert random data into the respective device table
        cursor.execute(f'''
            INSERT INTO device{device_id} (timestamp, temp, co2, fugt)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(), int(data.get('temperature')), int(data.get('co2_concentration')), int(data.get('humidity'))))

        # Retrieve the last 3 data points
        cursor.execute(f'''
            SELECT * FROM device{device_id}
            ORDER BY timestamp DESC
            LIMIT 8640
        ''')
        last_data_points = cursor.fetchall()

        # Delete all data from the table
        cursor.execute(f'''
            DELETE FROM device{device_id}
        ''')

        # Insert the last 3 data points back into the table
        for data_point in last_data_points:
            cursor.execute(f'''
                INSERT INTO device{device_id} (timestamp, temp, co2, fugt)
                VALUES (?, ?, ?, ?)
            ''', (data_point[1], data_point[2], data_point[3], data_point[4]))
        conn.commit()


def receivedPico():
    client_ip = request.remote_addr
    data = request.json
    print(f"Received Data:\nCO2: {data.get('co2_concentration')} ppm {data.get('co2_category')}\nTemp: {data.get('temperature')}°C\nHumidity: {data.get('humidity')}%")
    
    if client_ip == "192.168.1.3": #Skal måske ændres alt efter Pico's IP
        collect_and_insert_random_data(1)



@app.route('/')
def index():
    # Render the HTML template with the fetched data
    return render_template('index.html')

@app.route('/device1_POST', methods=['POST'])
def device1_POST():
    receivedPico()
    return "Success"

@app.route('/device1', methods=['GET'])
def device1():
    return render_template('device1.html')

@app.route('/device2')
def device2():
    return render_template('device2.html')

@app.route('/device3')
def device3():
    return render_template('device3.html')

@app.route('/api/device/1/latest_data', methods=['GET'])
def get_device1_latest_data():

    conn = sqlite3.connect('Picodata.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM device1
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    latest_data = cursor.fetchall()

    # Extracting the latest values
    latest_temp = [row[2] for row in latest_data]
    latest_co2 = [row[3] for row in latest_data]
    latest_fugt = [row[4] for row in latest_data]

    # response = requests.post(server_url, json=latest_data)

    return jsonify({
        'latest_temp': latest_temp,
        'latest_co2': latest_co2,
        'latest_fugt': latest_fugt,
    })

@app.route('/api/device/2/latest_data')
def get_device2_latest_data():
    with sqlite3.connect('Picodata.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM device2
            ORDER BY timestamp DESC
            LIMIT 3
        ''')
        latest_data = cursor.fetchall()

    # Extracting the latest values
    latest_temp = [row[2] for row in latest_data]
    latest_co2 = [row[3] for row in latest_data]
    latest_fugt = [row[4] for row in latest_data]

    return jsonify({
        'latest_temp': latest_temp,
        'latest_co2': latest_co2,
        'latest_fugt': latest_fugt
    })

@app.route('/api/device/3/latest_data')
def get_device3_latest_data():
    with sqlite3.connect('Picodata.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM device3
            ORDER BY timestamp DESC
            LIMIT 3
        ''')
        latest_data = cursor.fetchall()

    # Extracting the latest values
    latest_temp = [row[2] for row in latest_data]
    latest_co2 = [row[3] for row in latest_data]
    latest_fugt = [row[4] for row in latest_data]

    return jsonify({
        'latest_temp': latest_temp,
        'latest_co2': latest_co2,
        'latest_fugt': latest_fugt
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

