from .camera import Camera
from .colors import Colors
from .blobdetection import BlobDetector
from .thresholding import ColorDetectResult
from .window import Window

import math

class Vision(object):
	def __init__(self):
		"""Takes an image and returns the angle to blobs"""
		self.cam = Camera(544, 288)
		self.angle_to = 0
		self.debug_win = Window('vision debug')

		print self.cam.geom.wfov

	def update(self):
		self.frame = self.cam.read()
		self.color_detect = ColorDetectResult(self.frame)
		red_blobs = BlobDetector(self.color_detect, Colors.RED, 1000).blobs
		green_blobs = vision.BlobDetector(res, Colors.GREEN, 1000).blobs

		all_blobs = red_blobs + green_blobs

		self.debug_win.show(self.color_detect.debug_frame)\
		if all_blobs:
			max_blob = max(all_blobs, key=lambda b: b.area)
			ray = self.cam.geom.ray_at(max_blob.pos[1], max_blob.pos[0])
			self.angle_to = math.atan2(ray[0], ray[2])
		else:
			self.angle_to = 0