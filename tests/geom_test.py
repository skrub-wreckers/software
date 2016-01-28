from sw.vision import geometry
from sw import constants

import numpy as np


import unittest

class TestStringMethods(unittest.TestCase):
    def test_symmetry(self):
        g = constants.camera_geometry._replace(
            w=160, h=120, matrix=np.eye(4)
        )
        top_left = g.ray_at(0, 0)
        bottom_right = g.ray_at(160, 120)

        # compare the horizontal components
        np.testing.assert_allclose(top_left[1:3], -bottom_right[1:3],
            err_msg="corner rays are not symmetric")

    def test_angled(self):
        g = constants.camera_geometry._replace(w=160, h=120)
        print g.ray_at(80.0, 0)

        proj = [
        g.project_on(g.ray_at(80, 120), [0, 0, 1, 0], 0),
        g.project_on(g.ray_at(80, 50), [0, 0, 1, 0], 0)
        ]

        for p in proj:
            print(p)


    def test_matrix(self):
        g = constants.camera_geometry._replace(w=160, h=120)

        pixel = np.array([40, 20, 1])

        # project using the methods
        point = g.project_on(g.ray_at(*pixel[:2]), [0, 0, 1, 0], 0)

        #unproject using a matrix
        pixel2 = g.projection_matrix.dot(point)
        pixel2 = pixel2 / pixel2[-1]

        np.testing.assert_allclose(pixel, pixel2)

        # now project again with a matrix
        point2 = np.linalg.solve(
            np.vstack(
                (g.projection_matrix, [0, 0, 1, 0])
            ), np.append(
                pixel, 0
            )
        )
        self.assertGreater(point2[-1], 0)
        point2 = point2 / point2[-1]

        np.testing.assert_allclose(point, point2, atol=1e-9)

    def test_backwards_proj(self):
        m = np.eye(4)
        m[2,3] = 1
        g = constants.camera_geometry._replace(
            w=160, h=120, matrix=m
        )

        pixel = np.array([80, 0, 1])

        with self.assertRaises(ValueError):
            res = g.project_on(g.ray_at(*pixel[:2]), [0, 0, 1, 0], 0)

        point2 = np.linalg.solve(
            np.vstack(
                (g.projection_matrix, [0, 0, 1, 0])
            ), np.append(
                pixel, 0
            )
        )
        self.assertLess(point2[-1], 0)

if __name__ == '__main__':
    unittest.main()
