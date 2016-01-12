import numpy as np
import cv2, time
import scipy.ndimage
import scipy.signal


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


def threshold(frame, normal, d=0):
	""" returns true where the colors are above the plane defined by normal = [r, g, b] """
	normal = np.array(normal) / np.linalg.norm(normal)
	# bgr
	normal = normal[::-1]

	return np.dot(frame, normal) > d

def filter_smaller_than(area, mask):
	labelled, n_regions = scipy.ndimage.measurements.label(mask)
	small = [i for i in range(n_regions) if np.sum(labelled == i) < 100]
	for i in range(n_regions):
		match = labelled == i
		if np.sum(match) < 100:
			mask[match] = False

try:
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		if frame is None:
			print('No frame')
			continue

		is_red = (
			threshold(frame, [1, -0.65,  -0.65])
		)
		is_green = (
			threshold(frame, [-0.9, 1, -0.3])
		)
		is_blue = (
			threshold(frame, [-0.5, -0.65, 0.65])
		)

		if False:
			# remove pixels in both regions, classing them as neither
			multi = (is_red + is_green + is_blue) > 1
			is_red   = is_red & ~multi
			is_green = is_green & ~multi
			is_blue  = is_blue & ~multi

		is_black = threshold(frame, [-1, -1, -1], d=-64*1.71)

		# is_red   = is_red & ~is_black
		# is_green = is_green & ~is_black
		# is_blue  = is_blue & ~is_black


		is_white = ~is_blue & ~is_red & ~is_green & ~is_black

		# filter_smaller_than(100, is_red)
		# filter_smaller_than(100, is_green)



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
				all_data = np.concatenate(capData[c])
				np.save(c.name, all_data)

finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()