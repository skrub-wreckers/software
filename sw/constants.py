import numpy as np
from .vision.geometry import Geometry

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
    aspect = np.array([4, 3], dtype=np.float)
    aspect /= np.linalg.norm(aspect)

    fov = 2 * np.arctan(np.tan(diag_fov / 2) * aspect) # Calculate the FOV given the diagonal FOV

    # camera is tilted such that upper plane of FOV is parallel with ground
    tilt_down = fov[1] / 2
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

#Color sensor thresholds
nothingRange = 30
greenRange = 50
redRange = 120
colorRangeTolerance = 5

# favor gyro for disagreement (rad/s) above this
odometer_alpha = 0.2

#PID tuning
motorDistP = 0.15
motorDistI = 0
motorDistD = .0125

motorAngleP = 1.25
motorAngleI = 0
motorAngleD = 0.05

angleTolerance = 0.01
distanceTolerance = 0.01

round_time = 180

close_to_wall = 12

