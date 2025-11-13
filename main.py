import pyrealsense2 as rs
import cv2 as cv

class CameraSettings:
	def __init__(self, width, height, framerate):
		self.width = width
		self.height = height
		self.framerate = framerate

class Camera:
	def __init__(self, camera_settings):
		self.pipeline = rs.pipeline()
		self.config = rs.config()
		
		# Enable depth perception
		self.config.enable_stream(
			rs.stream.depth,
			camera_settings.width,
			camera_settings.height,
			rs.format.z16,
			camera_settings.framerate
		)
		
		self.pipeline.start(self.config)
		pass
	
	def process_frame_loop(self):
		try:
			while True:

				pass
		
		except Exception as err:
			print(err)
		
		finally:
			# Clean up and Stop Process
			self.pipeline.stop()

camera_settings = CameraSettings(640, 480, 30)
depth_camera = Camera(camera_settings)