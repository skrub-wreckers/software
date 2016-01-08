import numpy as np
import cv2

cap = cv2.VideoCapture(1)
cap.set(3, 480) #3=width
cap.set(4, 360) #4=height

try:
	while True:
		# Capture frame-by-frame
		ret, frame = cap.read()
			
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
		cv2.imshow('raw', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
finally:
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()