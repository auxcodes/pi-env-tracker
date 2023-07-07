import local_db as localdb

temperatures = []
humiditys = []
pressures = []
gases = []

def addReadings(reading):
    global temperatures
    global humiditys
    global pressures
    global gases
    if len(temperatures) < 6:
        temperatures.append(reading["temperature"])
        humiditys.append(reading["humidity"])
        pressures.append(reading["pressure"])
        gases.append(reading["gas"])
        print(len(temperatures))
    else:
        minuteAverage = averageReadings()
        localdb.insertMinuteReading(minuteAverage)
        clearReadings()
    
def averageReadings():
    global temperatures
    global humiditys
    global pressures
    global gases
    averages = { "temperature": None, "humidity": None, "pressure": None, "gas": None}
    averages["temperature"] = averageList(temperatures)
    averages["humidity"] = averageList(humiditys)
    averages["pressure"] = averageList(pressures)
    averages["gas"] = averageList(gases)
    return averages
    
def averageList(readingsList):
    average = 0
    for item in readingsList:
        average = average + item
    return average / 6
    
def clearReadings():
    global temperatures
    global humiditys
    global pressures
    global gases
    temperatures.clear()
    humiditys.clear()
    pressures.clear()
    gases.clear()
    
    


