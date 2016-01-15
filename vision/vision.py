import camera, constants, colors

class Vision(object):
	def __init__(self, cameraID):
		"""Takes an image and returns the angle to blobs"""
		self.cam = camera.Camera(544, 288)
		self.angle_to = 0
		
	def update(self):
		self.cam.read()
		res = vision.ColorDetectResult(self.cam.frame)
		red_blobs = vision.BlobDetector(res,  Colors.RED, 1000)
		#Terrible way to get real angle from screen coords
		if len(red_blobs)>0:
			max_size_id = 0
			for blob_id in range(0, len(red_blobs)):
				if red_blobs[blob_id].area > red_blobs[max_size_id].area:
					max_size_id = blob_id
			self.angle_to = constants.cameraFOV[0]*0.5*(red_blobs[max_size_id].pos[0]-(self.cam.shape[1]/2.0))