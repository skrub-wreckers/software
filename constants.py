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
    # from https://buntworthy.github.io/Wecam-field-of-views/
    diag_fov = np.radians(68)

    # aspect ratio, normalized
    aspect = np.array([3, 4])
    aspect /= np.linalg.norm(aspect)

    fov = 2 * np.arctan(np.tan(diag_fov) * aspect)

    # camera is tilted such that upper plane of FOV is parallel with ground
    tilt_down = np.radians(fov[1] / 2)
    z = 7  # inches off the ground

    return Geometry(
        w=320, h=240,
        wfov=fov[0], hfov=fov[1],
        matrix=np.array([
            [ np.cos(tilt_down), 0, np.sin(tilt_down), 0],
            [                 0, 1,                 0, 0],
            [-np.sin(tilt_down), 0, np.cos(tilt_down), z],
            [                 0, 0,                 0, 1]
        ])
    )
