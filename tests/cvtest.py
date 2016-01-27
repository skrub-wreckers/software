from __future__ import print_function
import time

import numpy as np
import cv2
import scipy.ndimage as ndimage

import sw.vision as vision
from sw.vision.colorselector import ColorSelector
from sw.vision.window import Window
from sw.vision.colors import Colors
from sw.util import Profiler

cam = vision.Camera(w=544, h=288, debug=False, id=1)

selector = ColorSelector(cam.shape)
result_win = Window('result')


fRec = 0
lastCap = 0


try:
	while True:
		# Capture frame-by-frame
		try:
			frame = cam.read()
		except IOError:
			print('No frame')
			continue
		with Profiler('all') as profiler:
			with profiler('detect') as p:
				res = vision.ColorDetectResult(frame)
			with profiler('bluecut') as p:
				is_blue = (res.im == Colors.BLUE)
				is_blue = ndimage.binary_opening(is_blue, structure=np.ones((5,5)))
				is_blue = ndimage.binary_closing(is_blue, structure=np.ones((5,5)))

				x, y = np.meshgrid(np.arange(cam.shape[1]), np.arange(cam.shape[0]))

				blue_below = np.cumsum(is_blue[::-1], axis=0)[::-1]
				res.mask_out((blue_below > 0) & ~is_blue)
			with Profiler('fill'):
				red_blobs = vision.BlobDetector(res,  Colors.RED, 1000)
				green_blobs = vision.BlobDetector(res, Colors.GREEN, 1000)
				blue_blobs = vision.BlobDetector(res, Colors.BLUE, 2000)

		frame = np.copy(frame)
		for blob in red_blobs.blobs + blue_blobs.blobs + green_blobs.blobs:
			y, x = blob.pos
			color = tuple(map(int, Colors.to_rgb(blob.color)))
			cv2.circle(frame, (int(x), int(y)), 20, color, thickness=-1)




		# gradx = ndimage.filters.sobel(is_blue, 0)
		# grady = ndimage.filters.sobel(is_blue, 1)
		# hyp = np.hypot(gradx, grady)
		# hyp = hyp / float(np.max(hyp))
		# hyp = hyp[...,np.newaxis]

		debug = res.debug_frame
		# for x1, y1, x2, y2 in lines:
		# 	cv2.line(debug, (x1,y1), (x2,y2), [0, 0, 128], thickness=2)

		# debug[above_blue,:] = debug[above_blue,:] * 0.125


		result_win.show(debug)
		selector.show(frame)

		if time.time() - lastCap > 1 and fRec > 0:
			selector.record(frame)
			fRec -= 1
			print(fRec)
			lastCap = time.time()

		c = cv2.waitKey(1) & 0xFF
		if c == ord('q'):
			break
		elif c == ord('r'):
			selector.clear()
			fRec = 10
			lastCap = time.time()
		elif c == ord('n'):
			selector.next_color()
			print("Editing {} mask".format(selector.active_color.name))
		elif c == ord('s'):
			selector.save('color-data')

finally:
	# When everything done, release the capture
	cam.close()
	cv2.destroyAllWindows()