from __future__ import print_function

import numpy as np
import cv2, time

import vision
from vision.colorselector import ColorSelector
from vision.window import Window
from vision.colors import Colors


from util import Timer

cam = vision.Camera(w=544, h=288, debug=False)

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

		with Timer('all') as timer:
			with timer('detect') as timer:
				res = vision.ColorDetectResult(frame)

			with timer('fill'):
				red_blobs = vision.BlobDetector(res,  Colors.RED, 1000)
				green_blobs = vision.BlobDetector(res, Colors.GREEN, 1000)
				blue_blobs = vision.BlobDetector(res, Colors.BLUE, 2000)

		frame = np.copy(frame)
		for blob in red_blobs.blobs + blue_blobs.blobs + green_blobs.blobs:
			y, x = blob.pos
			color = tuple(map(int, Colors.to_rgb(blob.color)))
			cv2.circle(frame, (int(x), int(y)), 20, color, thickness=-1)


		result_win.show(res.debug_frame)
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