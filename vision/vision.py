from .camera import Camera
from .colors import Colors
from .blobdetection import BlobDetector
from .thresholding import ColorDetectResult
from .window import Window

import math

class Vision(object):
	def __init__(self, cam):
		"""Takes an image and returns the angle to blobs"""
		self.cam = cam
		self.ray = None
		self.angle_to = None
		self.debug_win = Window('vision debug')

	def update(self):
		self.frame = self.cam.read()
		self.color_detect = ColorDetectResult(self.frame)
		red_blobs = BlobDetector(self.color_detect, Colors.RED, 100).blobs
		green_blobs = BlobDetector(self.color_detect, Colors.GREEN, 100).blobs

		all_blobs = red_blobs + green_blobs

		self.debug_win.show(self.color_detect.debug_frame)
		if all_blobs:
			max_blob = max(all_blobs, key=lambda b: b.area)

			self.ray = self.cam.geom.ray_at(max_blob.pos[1], max_blob.pos[0])
			self.angle_to = math.atan2(self.ray[1], self.ray[0])
		else:
			self.ray = None
			self.angle_to = None

	@property
	def block_pos(self):
		if self.ray is None: return
		# project onto the cube midplane
		return self.cam.geom.project_on(self.ray, [0, 0, 1, 0], 1)[:2]
