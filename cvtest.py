import numpy as np
import cv2, time

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 544)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

cv2.namedWindow("raw")

mask = np.zeros((288, 544))

fRec = 0
lastCap = 0
capData = []

# paint the mask with left and right click
drawing = None
def on_click(event,x,y,flags,param):
    global drawing

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

def threshold(normal, frame):
	""" returns true where the colors are above the plane defined by normal = [r, g, b] """
	normal = np.array(normal) / np.linalg.norm(normal)
	# bgr
	normal = normal[::-1]

	return np.dot(frame, normal) > 0

try:
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		if frame is None:
			print('No frame')
			continue

		is_red = (
			threshold([1, -1.3,  0], frame) &
			threshold([1,    0, -1.3], frame)
		)
		is_green = (
			threshold([-1.3, 1,  0], frame) &
			threshold( [0,   1, -1.3], frame)
		)

		diagnostic = np.zeros(frame.shape).astype(np.uint8)
		diagnostic[...,R] = is_red * 255
		diagnostic[...,G] = is_green * 255

		cv2.imshow('filtered',diagnostic)

		# flash the mask on and off
		if time.time() %0.5 < 0.25:
			mod = np.where(mask[...,np.newaxis], 255-frame, frame)
		else:
			mod = frame

		cv2.imshow('raw', mod)

		if time.time() - lastCap > 1 and fRec > 0:
			capData.append(frame[mask.astype(np.bool),:])
			fRec -= 1
			print fRec
			lastCap = time.time()

		#if colDisp.shape
		#cv2.imshow('Selected colors', colDisp)

		c = cv2.waitKey(1) & 0xFF
		if c == ord('q'):
			break
		elif c == ord('r'):
			fRec = 10
			lastCap = time.time()
		elif c == ord('s'):
			all_data = np.concatenate(capData)
			np.save('out', all_data)

finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()