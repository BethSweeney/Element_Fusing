from vmbpy import *
import cv2
import numpy as np

class CameraComms():

    def __init__(self, number_images:int,frames_list):
        self.single_frame()
        frames = self.multiple_frames(number_images)
        save_as_image(frames)


    ## get single frame
    def single_frame(self)-> None:
        
        with VmbSystem.get_instance() as vmb:
        cams = vmb.get_all_cameras()
        with cams[0] as cam:
                # Aquire single frame synchronously
                frame = cam.get_frame()
                print('Got {}'.format(frame), flush=True)


    ## get multiple frames
    def multiple_frames(self,number_images):
        frames_list = []

        with VmbSystem.get_instance() as vmb:
            cams = vmb.get_all_cameras()

            with cams[0] as cam:
                for frame in cam.get_frame_generator(limit=number_images):
                    frames_list.append(frame)
                    print('Got {}'.format(frame), flush=True)
                return frames_list


    ## save frames as images
    def save_as_image(self,frames_list)-> None:
        
        for i, f in enumerate(frames_list):
            f.convert_pixel_format(PixelFormat.Mono8)
            cv2.imwrite(f'./frame{i}.png', f.as_opencv_image())
