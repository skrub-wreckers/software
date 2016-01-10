import numpy as np
import cv2, time, pickle

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

try:
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
		if frame is None:
			print('No frame')
			continue

		is_red = (frame[...,2] > 1.3*frame[...,1]) & (frame[...,2] > 1.3*frame[...,0]);

		red_im = (is_red * 255).astype(np.uint8)

		cv2.imshow('filtered',red_im)

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
			f = open("out.dat", "w")
			pickle.dump(np.concatenate(capData), f)
			f.close()
	
finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()