#Script designed for a sensor node that reads temperature, pressure, and RPM, then logs them 
#with a timestamp. Uses a loop for periodic readings for capturing data and then will print onto the console. 

import time
import random
from datetime import datetime

#Sensor Node - Data Script

def read_temperature():
    #Simulate temperature reading in Celsius
    return round(random.uniform(20.0, 30.0), 2)

def read_pressure():
    #Simulate temperature reading in Celsius
    return round(random.uniform(1000.0, 1015.0), 2)

def read_rpm():
    #Simulate RPM reading
    return random.randint(1000, 3000)

def main():
    try:
        while True:
            # Get Timestamps
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Reads Sensors
            temp = read_temperature()
            press = read_pressure()
            rpm = read_rpm()

            # Format and Print Data
            data_str = f"{timestamp} | Temperature: {temp} °C | Pressure: {press} hPa | RPM: {rpm}"
            print(data_str)

            # Give option to log to a file
            # with open("sensor_log.csv", "a") as f:
            #    f.write(f"{timestamp},{temp},{press},{rpm}\n")

    except KeyboardInterrupt:
        print("\nSensor node stopped.")

if __name__ == "__main__":
    main()