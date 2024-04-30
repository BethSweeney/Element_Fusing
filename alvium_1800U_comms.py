from vmbpy import *
import cv2
import numpy as np
from time import sleep
import os

class CameraComms():

    def __init__(self) :#number_images:int,image_every_x_seconds:int):
        self.single_frame()
        #frames = self.multiple_frames(number_images,image_every_x_seconds)
        #self.save_as_image(frames)


    ## get single frame
    def single_frame(self)-> None:
        
        with VmbSystem.get_instance() as vmb:
            cams = vmb.get_all_cameras()
            with cams[0] as cam:
                # Aquire single frame synchronously
                frame = cam.get_frame()
                print('Got {}'.format(frame), flush=True)


    ## get multiple frames
    def multiple_frames(self,number_images,image_every_x_seconds):
        global frames_list
        frames_list = []

        with VmbSystem.get_instance() as vmb:
            cams = vmb.get_all_cameras()

            with cams[0] as cam:
                for frame in cam.get_frame_generator(limit=number_images):
                    frames_list.append(frame)
                    print('Got {}'.format(frame), flush=True)
                    sleep(image_every_x_seconds)
                return frames_list


    ## save frames as images
    def save_as_image(self,cam_filepath)-> None:
        directory=cam_filepath
        os.mkdir(directory)
        for i, f in enumerate(frames_list):
            frame1 = f.as_numpy_ndarray()
        ## converts from rgb8 to open cv pixel format (needs array as first parameter)
            #os.chdir(directory) 
            f = cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR)         
            cv2.imwrite(directory+f'\\frame{i}.png', f)
