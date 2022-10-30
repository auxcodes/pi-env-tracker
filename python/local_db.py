import sqlite3
from datetime import datetime

dbconn = None
minuteCount = 0
thirtyMinuteCount = 0

def dbConnect():
    global dbconn
    dbconn = sqlite3.connect('./db/env-tracker.db')
    try:
        dbconn.execute("CREATE TABLE minute_readings (datetime integer, temperature real, humidity real, pressure real, gas real)")
    except sqlite3.Error as error:
        print("!! SQLite Error: ", error, '\n')
    try:
        dbconn.execute("CREATE TABLE thirty_minute_readings (datetime integer, temperature real, humidity real, pressure real, gas real)")
    except sqlite3.Error as error:
        print("!! SQLite Error: ", error, '\n')
        
def lastMinuteReading():
    global dbconn
    cur = dbconn.cursor()
    cur.execute("SELECT * FROM minute_readings ORDER BY ROWID DESC LIMIT 1")
    print(cur.fetchall())
    cur.close()
    
def insertMinuteReading(reading):
    global dbconn
    global minuteCount
    if (dbconn):
        now = datetime.utcnow()
        try:
            with dbconn:
                if (minuteCount < 30):
                    dbconn.execute("INSERT INTO minute_readings VALUES(?,?,?,?,?)", (now, reading["temperature"], reading["humidity"], reading["pressure"], reading["gas"]))
                    print(f"Insert {minuteCount} minute reading...")
                    minuteCount = minuteCount + 1
                    print("Current averages: ", averageMinuteReadings())
                else:
                    thirtyMinuteAverages = averageMinuteReadings()
                    insertThirtyMinuteReading(thirtyMinuteAverages)
                    minuteCount = 0
                    clearMinuteReadings()
                    print("Thirty minute average...")
        except sqlite3.IntegrityError:
            print("Error inserting minute data")

def printMinuteContents():
    global dbconn
    if (dbconn):
        cur = dbconn.cursor()
        cur.execute("SELECT * FROM minute_readings")
        print(cur.fetchall())
        cur.close()
        dbconn.close()
        print("The SQLite connection is closed")
    else:
        print("No SQLite connection to print")
        
def averageMinuteReadings():
    global dbconn
    global thirtyMinuteCount
    cur = dbconn.cursor()
    temperature = cur.execute("SELECT AVG(temperature) FROM minute_readings").fetchone()[0]
    humidity = cur.execute("SELECT AVG(humidity) FROM minute_readings").fetchone()[0]
    pressure = cur.execute("SELECT AVG(pressure) FROM minute_readings").fetchone()[0]
    gas = cur.execute("SELECT AVG(gas) FROM minute_readings").fetchone()[0]
    temperature = average(thirtyMinuteCount, temperature)
    humidity = average(thirtyMinuteCount, humidity)
    pressure = average(thirtyMinuteCount, pressure)
    gas = average(thirtyMinuteCount, gas)
    print("AVG - Temp = {0:0.1f} C, Humidity = {1:0.1f} %, Pressure = {2:0.1f} hPa, Gas = {3:0.1f} ohms".format(temperature, humidity, pressure, gas))
    cur.close()
    return { "temperature": temperature, "humidity": humidity, "pressure": pressure, "gas": gas}

def average(count, value):
    if (count > 0):
        return value / count
    else:
        return value

def clearMinuteReadings():
    global dbconn
    cur = dbconn.cursor()
    cur.execute("DELETE FROM minute_readings")
    print("Clear minute database readings...")
    cur.close()
    
def insertThirtyMinuteReading(reading):
    global dbconn
    global thirtyMinuteCount
    if (dbconn):
        now = datetime.utcnow()
        try:
            with dbconn:
                if (thirtyMinuteCount < 48):
                    dbconn.execute("INSERT INTO thirty_minute_readings VALUES(?,?,?,?,?)", (now, reading["temperature"], reading["humidity"], reading["pressure"], reading["gas"]))
                    print(f"Insert {thirtyMinuteCount} thirty minute reading...", datetime.now())
                    thirtyMinuteCount = thirtyMinuteCount + 1
                else:
                    thirtyMinuteCount = 0
                    clearMinuteReadings()
                    print("24 Hours done...", datetime.now())
        except sqlite3.IntegrityError:
            print("Error inserting thirty minute data")
            
def clearThirtyMinuteReadings():
    global dbconn
    cur = dbconn.cursor()
    cur.execute("DELETE FROM thirty_minute_readings")
    print("Clear thirty minute database readings...")
    cur.close()
