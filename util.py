def threshold(normal, frame):
	""" returns true where the colors are above the plane defined by normal = [r, g, b] """
	normal = np.array(normal) / np.linalg.norm(normal)
	# bgr
	normal = normal[::-1]

	return np.dot(frame, normal) > 0

def clamp(value, min, max):
	if value < min: 
		return min
	elif value > max:
		return max
	else:
		return value