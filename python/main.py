import pyrealsense2 as rs
import numpy as np
import cv2
import yolov5 as yv5
import os
import psutil


def array_to_text(np_array):
    # Flatten to 1D, convert to strings, join with commas
    flat = np_array.flatten()
    return ",".join(map(str, flat))

class TrainingMgr:
    def __init__(self, path_to_data):
        if not os.path.exists(path_to_data):
            print("File does not exists!")
            return None
        
        self.path_to_data = path_to_data

        self.image_data = []
        self.crumpled_data = []
        self.combined_data = []
        pass

    def collect_data(self, np_data_array, crumpled):
        self.image_data.append(np_data_array) # Array of array of images
        self.crumpled_data.append(crumpled) # Array of crumple status
        self.combined_data.append([array_to_text(np_data_array), str(crumpled)])
        pass

    def get_memory_usage(self):
        process = psutil.Process()
        mem = process.memory_info().rss  # in bytes
        print(f"Memory usage: {mem / 1024**2:.2f} MB")
        pass

    def cleanup_and_save(self):
        with open(self.path_to_data, "a") as file:
            for data in self.combined_data:
                file.write(f"{data[0]}|{data[1]}\n")


class Resolution:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CameraSettings:
    def __init__(self, resolution, framerate):
        self.resolution = resolution
        self.framerate = framerate

class Camera:
    def __init__(self, camera_settings, screenshot_crumpled_key, screenshot_uncrumpled_key, training_mgr):
        self.camera_settings = camera_settings
        self.screenshot_crumpled_key = screenshot_crumpled_key
        self.screenshot_uncrumpled_key = screenshot_uncrumpled_key
        self.training_mgr = training_mgr

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.camera_settings.resolution.x, self.camera_settings.resolution.y, rs.format.bgr8, 5)
        self.profile = self.pipeline.start(self.config)
        self.align = rs.align(rs.stream.color)

    def camera_process(self):
        try:
            while True:
                frames = self.pipeline.wait_for_frames()
                aligned_frames = self.align.process(frames)

                color_frame = aligned_frames.get_color_frame()

                if not color_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())
 
                cv2.imshow("Image", color_image)

                key = cv2.waitKey(1)
                if key == 27:  #resolution ESC to exit
                    break

                if key == self.screenshot_crumpled_key:
                    print("Taken photo crumpled")
                    self.training_mgr.collect_data(color_image, True)
                    pass

                elif key == self.screenshot_uncrumpled_key:
                    print("Taken photo uncrumpled")
                    self.training_mgr.collect_data(color_image, False)
                    pass

                elif key == 77:
                    self.training_mgr.get_memory_usage()
                    pass

        finally:
            self.pipeline.stop()
            cv2.destroyAllWindows()
        

def main():
    training_mgr = TrainingMgr("data.txt")
    res = Resolution(1280, 720)
    camera_settings = CameraSettings(resolution=res, framerate=30)
    
    # 1 - crumpled, 2 - uncrumpled
    camera = Camera(camera_settings, screenshot_crumpled_key=49, screenshot_uncrumpled_key=50, training_mgr=training_mgr)
    
    camera.camera_process() # Starts camera process loop
    
    camera.training_mgr.cleanup_and_save()
    pass

if __name__ == "__main__":
    main()