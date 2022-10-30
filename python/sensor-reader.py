import board
import adafruit_bme680

import time
import datetime
import sqlite3

import local_db as localdb
import temp_data as tempdata
 
try:
    sensor = adafruit_bme680.Adafruit_BME680_I2C(board.I2C())
except IOError:
    print("!! SQLite Error: ", error, '\n')
    sensor = { "temperature": -99, "humidity": -99, "pressure": -99, "gas": -99}

localdb.dbConnect()
localdb.clearMinuteReadings()
localdb.clearThirtyMinuteReadings()

while True:
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        pressure = sensor.pressure
        gas = sensor.gas
        
        if temperature is not None:
            print("RT - Temp = {0:0.1f} C, Humidity = {1:0.1f} %, Pressure = {2:0.1f} hPa, Gas = {3:0.1f} ohms".format(temperature, humidity, pressure, gas))
            tempdata.addReadings({"temperature": temperature, "humidity": humidity, "pressure": pressure, "gas": gas})
        else:
            print("Sensor failure. Check wiring.");

        time.sleep(10);
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

localdb.printMinuteContents()
