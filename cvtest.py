from __future__ import print_function

import numpy as np
import cv2, time
import scipy.ndimage
import scipy.signal


class Timer():
	def __init__(self, name, indent=''):
		self.name = name
		self.indent = indent
		self.has_children = False

	def __enter__(self):
		self.t = time.time()
		print(self.indent +'Timing {}... '.format(self.name), end='')
		return self

	def __exit__(self, *args):
		if self.has_children:
			print()
			print(self.indent + '  ' + str(time.time() - self.t))
		else:
			print(str(time.time() - self.t))

	def __call__(self, name):
		print()
		self.has_children = True
		return Timer(name, self.indent + '  ')



cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 544)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

cv2.namedWindow("raw")

mask = np.zeros((288, 544))
class ColorData(object):
	def __init__(self, name, ui_bgr):
		self.ui_bgr = np.array(ui_bgr)
		self.name = name
		self.mask = np.zeros((288, 544))

colors = [
	ColorData('red',   [0, 0, 255]),
	ColorData('green', [0, 255, 0]),
	ColorData('blue',  [255, 0, 0]),
	ColorData('black',  [32, 32, 32]),
	ColorData('white',  [192, 192, 192])
]

color_i = 0


fRec = 0
lastCap = 0
capData = {c: [] for c in colors}

# paint the mask with left and right click
drawing = None
def on_click(event,x,y,flags,param):
	global drawing

	mask = colors[color_i].mask

	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = 'set'
	elif event == cv2.EVENT_RBUTTONDOWN:
		drawing = 'right'

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing != None:
			cv2.circle(mask, (x,y), 5, 1 if drawing == 'set' else 0, -1)

	elif event == cv2.EVENT_LBUTTONUP:
		cv2.circle(mask, (x,y), 5, 1 if drawing == 'set' else 0, -1)
		drawing = None

	elif event == cv2.EVENT_RBUTTONUP:
		cv2.circle(mask, (x,y), 5, 1 if drawing == 'set' else 0, -1)
		drawing = None

cv2.setMouseCallback("raw", on_click)

R = 2
G = 1
B = 0

edge_kernel = np.array([
	[0, 1, 0],
	[1, 0, 1],
	[0, 1, 0]
])

def highlight_region(frame, mask, color):
	color = np.array(color)
	bmask = mask.astype(np.bool)

	border = bmask & (scipy.signal.convolve2d(mask, edge_kernel, mode='same') != 4)
	mod = np.copy(frame)
	mod[bmask, :] = mod[bmask, :] * 0.5 + color * 0.25 + 0.25
	mod[border,:] = color
	return mod


class Thresholder(object):
	def __init__(self, normal, d):
		normal = np.array(normal) / np.linalg.norm(normal)
		# bgr
		self.normal = normal[::-1]
		self.d = d

	def apply(self, frame):
		return np.dot(frame, self.normal) > self.d

def filter_smaller_than(area, mask):
	labelled, n_regions = scipy.ndimage.measurements.label(mask)
	small = [i for i in range(n_regions) if np.sum(labelled == i) < 100]
	for i in range(n_regions):
		match = labelled == i
		if np.sum(match) < 100:
			mask[match] = False

thresh_red   = Thresholder([1, -0.65,  -0.65], 16)
thresh_green = Thresholder([-0.9, 1, -0.3], 4)
thresh_blue  = Thresholder([-0.3, -0.9, 1], 8)
thresh_black = Thresholder([-1, -1, -1], -130)

try:
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		if frame is None:
			print('No frame')
			continue

		with Timer('all') as timer:
			with timer('thresholding'):
				is_red = (
					thresh_red.apply(frame)
				)
				is_green = (
					thresh_green.apply(frame)
				)
				is_blue = (
					thresh_blue.apply(frame)
				)
				is_black = thresh_black.apply(frame)

			with timer('logic'):
				is_green = is_green & ~is_blue
				is_white = ~is_blue & ~is_red & ~is_green & ~is_black


			with timer('blobs'):
				filter_smaller_than(100, is_red)
				filter_smaller_than(100, is_green)



		diagnostic = np.zeros(frame.shape).astype(np.uint8)
		diagnostic[...,R] = (is_white | is_red) * 255
		diagnostic[...,G] = (is_white | is_green) * 255
		diagnostic[...,B] = (is_white | is_blue) * 255
		
		cv2.imshow('filtered',diagnostic)

		mod = frame
		for color in colors:
			mod = highlight_region(mod, color.mask, color.ui_bgr)

		cv2.imshow('raw', mod)

		if time.time() - lastCap > 1 and fRec > 0:
			for c in colors:
				capData[c].append(frame[c.mask.astype(np.bool),:])
			fRec -= 1
			print(fRec)
			lastCap = time.time()

		#if colDisp.shape
		#cv2.imshow('Selected colors', colDisp)

		c = cv2.waitKey(1) & 0xFF
		if c == ord('q'):
			break
		elif c == ord('r'):
			fRec = 10
			lastCap = time.time()
		elif c == ord('n'):
			color_i = (color_i + 1) % len(colors)
			print("Editing {} mask".format(colors[color_i].name))
		elif c == ord('s'):
			for c in colors:
				if capData[c]:
					all_data = np.concatenate(capData[c])
					np.save(c.name, all_data)

finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()