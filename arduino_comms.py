import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import serial
import time

class ArduinoComms():
    global ser

    def __init__(self, port:str ,baud:int):
        self.connect_arduino(port,baud)

    def connect_arduino(self,port,baud)-> None:
        global ser

        ser = serial.Serial(port,baud)
        print("Connected to Arduino port:" + port)


    def collect_current_and_temp(self,collection_duration, start_time):
        global ser
        global sensor_data
        sensor_data = []
        while (time.time() - start_time) <= collection_duration:
            getData = ser.readline()                  # Read data from Arduino serial monitor
            dataString = getData.decode('utf-8')      # Convert from bytes to string
            data = dataString.rstrip()                # Get rid of \r\n 

            sensor_data.append(data)
        return sensor_data
    

    ## function to write  data to file
    def write_to_file(self,fileName)-> None:
        file = open(fileName, "a")

        index_data = np.arange(0,len(sensor_data)-1,1)    
        with open(fileName,'a') as data_file:
            for i in index_data:
                data_file.write(str(sensor_data[i])+'\n')
        
        print("Data collection complete!")
        file.close()