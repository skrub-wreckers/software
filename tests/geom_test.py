from sw.vision import geometry
from sw import constants

import numpy as np

g = constants.camera_geometry._replace(
    w=160, h=120, matrix=np.eye(4)
)

top_left = g.ray_at(0, 0)
bottom_right = g.ray_at(160, 120)

# compare the horizontal components
assert (top_left[1:] == -bottom_right[1:]).all()



g = constants.camera_geometry._replace(w=160, h=120)

print g.ray_at(80.0, 0)

proj = [
g.project_on(g.ray_at(80, 120), [0, 0, 1, 0], 0),
g.project_on(g.ray_at(80, 50), [0, 0, 1, 0], 0)
]

for p in proj:
    print(p)

print "--"

pixel = np.array([40, 20, 1])

p = g.project_on(g.ray_at(*pixel[:2]), [0, 0, 1, 0], 0)
print p
print np.linalg.inv(g.matrix).dot(p)
res = g.projection_matrix.dot(p)
res = res / res[-1]


proj2 = np.linalg.solve(
    np.vstack(
        (g.projection_matrix, [0, 0, 1, 0])
    ), np.append(
        pixel, 0
    )
)
proj2 = proj2 / proj2[-1]
print res, pixel
print p, proj2
