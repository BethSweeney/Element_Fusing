## import classes
from alvium_1800U_comms import CameraComms
from mfg2110_comms import MFG2110Comms
from arduino_comms import ArduinoComms

## import arduino packages
import serial
import csv 
import numpy as np
import threading
import time
import matplotlib.pyplot as plt
from time import sleep
import os

# Set up place to store data
os.mkdir(r"C:\Users\beth_\Documents\Element_Fusing\Arduino_temp_current_sensor\12_04\sandwich_slow_off")
os.mkdir(r"C:\Users\beth_\Documents\Element_Fusing\main_script\camera_images\12_04_camera\sandwich_slow_off")


file_directory = r"C:\Users\beth_\Documents\Element_Fusing\Arduino_temp_current_sensor\12_04\sandwich_slow_off"
camera_directory = r"C:\Users\beth_\Documents\Element_Fusing\main_script\camera_images\12_04_camera\sandwich_slow_off"


#### SET UP COMMS #################################################################################

my_arduino = ArduinoComms(port='COM4',baud= 115200)
my_mfg2110 = MFG2110Comms(port='COM3',baudrate= 115200, timeout= 6)
my_camera = CameraComms()


## Function to start run 
def start_run(current,resistance, time_frame,filepath,cam_file_path,no_cam_images,image_every_x_sec)-> None:
    
    #my_mfg2110.send_signal(wave='SIN',frequency='341.5HZ',amplitude='0',offset='0')
    #my_arduino.collect_current_and_temp(collection_duration=20,start_time=time.time())
    #my_arduino.write_to_file(file_directory+filepath)
    #os.mkdir(directory)

    #volt = (current*resistance)/2
    #my_mfg2110.send_signal(wave='SIN',frequency='341.5HZ',amplitude=str(volt),offset='0')

    collection_time = time_frame
    start= time.time()
    frames = my_camera.multiple_frames
    Data = my_arduino.collect_current_and_temp

    thread_current = threading.Thread(target=Data,args=(collection_time,start))
    thread_camera = threading.Thread(target= frames, args=(no_cam_images,image_every_x_sec))

    thread_current.start()
    thread_camera.start()
    thread_current.join()
    thread_camera.join()

    #my_mfg2110.send_signal(wave='SIN',frequency='341.5HZ',amplitude='0',offset='0')
    #my_mfg2110.close_comms()

    my_camera.save_as_image(cam_file_path)
    my_arduino.write_to_file(file_directory+filepath)



### Call function
    
#start_run(100e-3,1*60,"\\test11.txt",camera_directory+'\\long_run_thin_1',1,1*60)
#
#range_currents = np.arange(750e-3,2,25e-3)
#
range_i = np.arange(0,1500,1)
volt = (1*11)/2
my_mfg2110.send_signal(wave='SIN',frequency='341.5HZ',amplitude=str(volt),offset='0')
#print(volt)
   
#os.mkdir(file_directory+f"\\fuse_break_test.txt")
file = open(file_directory+f"\\sandwich_slow_off.txt", "w")
#file.close()

for i in range_i:  
  start_run(i,11,1*60,f"\\sandwich_slow_off.txt",camera_directory+f"\\sandwich_slow_off{i}",1,10)
  print(i)

#start_run(200e-3,9,1*60,f"\\test6.txt",camera_directory+f"\\test7",1,10)
  
my_mfg2110.send_signal(wave='SIN',frequency='341.5HZ',amplitude='0',offset='0')
print('Finished!')
