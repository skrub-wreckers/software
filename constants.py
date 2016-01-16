import numpy as np
from vision.geometry import Geometry

_calculated = lambda f: f()

#Camera constants
cameraID = 1
cameraDebug = True

#CV constants
planes = {"red":[[1, -1.3, 0], [1, 0, -1.3]],
		"green":[[-1.3, 1, 0], [0, 1, -1.3]],
		"blue":[[-0.5, -0.65, 0.65]]}

@_calculated
def camera_geometry():
    fov = (54.4, 40.8)
    # camera is tilted such that upper plane of FOV is parallel with ground
    tilt_down = np.radians(fov[1] / 2)
    z = 6.5  # 6.5 inches off the ground

    return Geometry(
        w=544, h=288,
        wfov=fov[0], hfov=fov[1],
        matrix=np.array([
            [ np.cos(tilt_down), 0, np.sin(tilt_down), 0],
            [                 0, 1,                 0, 0],
            [-np.sin(tilt_down), 0, np.cos(tilt_down), z],
            [                 0, 0,                 0, 1]
        ])
    )
