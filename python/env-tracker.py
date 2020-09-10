import Adafruit_DHT
import time
import datetime
import sqlite3
#import keyboard
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
conn = sqlite3.connect('../env-tracker.db')
try:
    conn.execute("create table readings (datetime integer, temperature real, humidity real)")
except sqlite3.Error as error:
    print("Table already exists: ", error)


while True:
    try:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            now = datetime.datetime.now()
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
            try:
                with conn:
                    conn.execute("insert into readings values(?,?,?)", (now, temperature, humidity))
            except sqlite3.IntegrityError:
                print("Error inserting data")
        else:
            print("Sensor failure. Check wiring.");
        #if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        #    print('You Pressed A Key!')
        #    break  # finishing the loop
        time.sleep(10);
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
        
if (conn):
    cur = conn.cursor()
    cur.execute("select * from readings")
    print(cur.fetchall())
    cur.close()
    conn.close()
    print("The SQLite connection is closed")

