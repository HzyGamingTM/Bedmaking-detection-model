import pyrealsense2 as rs
import numpy as np
import cv2
import yolov5 as yv5
import os
import psutil

class TrainingMgr:
    def __init__(self):
        self.counter = 0 
        pass

    def collect_data(self, image_data, crumpled):
        crumpled_status = "error"
        if crumpled:
            crumpled_status = "crumpled"
        else:
            crumpled_status = "uncrumpled"

        filename = f"{str(self.counter)}_{crumpled_status}.png"
        output_path = os.path.join("data", filename)
        cv2.imwrite(output_path, image_data)
        print(f"Saved as {filename}")
        self.counter += 1
        pass

    def get_memory_usage(self):
        process = psutil.Process()
        mem = process.memory_info().rss  # in bytes
        print(f"Memory usage: {mem / 1024**2:.2f} MB")
        pass


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
                    print("Taken photo | Crumpled")
                    self.training_mgr.collect_data(color_image, True)
 

                elif key == self.screenshot_uncrumpled_key:
                    print("Taken photo | Uncrumpled")
                    self.training_mgr.collect_data(color_image, False)

                elif key == 77:
                    print("Getting Memory")
                    self.training_mgr.get_memory_usage()
                    
        finally:
            self.pipeline.stop()
            cv2.destroyAllWindows()
        

def main():
    training_mgr = TrainingMgr()
    res = Resolution(1280, 720)
    camera_settings = CameraSettings(resolution=res, framerate=30)
    
    # 1 - crumpled, 2 - uncrumpled
    camera = Camera(camera_settings, screenshot_crumpled_key=49, screenshot_uncrumpled_key=50, training_mgr=training_mgr)
    
    camera.camera_process() # Starts camera process loop
    pass

if __name__ == "__main__":
    main()