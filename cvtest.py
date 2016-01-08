import numpy as np
import cv2
import time

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 544) #3=width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288) #4=height


cv2.namedWindow("raw")

mask = np.zeros((288, 544))


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

		#test = cv2.compare(frame[:,:,2], 13*(frame[:,:,1]/10), cv2.CMP_GT)
		#test2 = cv2.compare(frame[:,:,2], 13*(frame[:,:,0]/10), cv2.CMP_GT)
		#test3 = cv2.add(test/2, test2/2)
		#test4 = cv2.compare(test3, 200, cv2.CMP_GT)

		# test = cv2.compare(frame[:,:,1], 13*(frame[:,:,2]/10), cv2.CMP_GT)
		# test2 = cv2.compare(frame[:,:,1], 11*(frame[:,:,0]/10), cv2.CMP_GT)
		# test3 = cv2.add(test/2, test2/2)
		# test4 = cv2.compare(test3, 200, cv2.CMP_GT)


		is_red = (frame[...,2] > 1.3*frame[...,1]) & (frame[...,2] > 1.3*frame[...,0]);

		red_im = (is_red * 255).astype(np.uint8)

		cv2.imshow('frame',red_im)

		# flash the mask on and off
		if time.time() %0.5 < 0.25:
			frame = np.where(mask[...,np.newaxis], 255-frame, frame)

		cv2.imshow('raw', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()