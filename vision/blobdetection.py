from collections import namedtuple

import numpy as np
import scipy.ndimage

Blob = namedtuple('Blob', 'color pos area')

class BlobDetector(object):
    def __init__(self, color_detect_result, color, min_area):
        """
        Detect blobs from a ColorDetectResult object, of a given color and minimum area

        self.blobs is a list of Blob objects, containing .pos == (x,y), .color, and .area
        """
        mask = color_detect_result.im == color
        labelled, n_regions = scipy.ndimage.measurements.label(mask)

        self.labelled = labelled
        self.n_regions = n_regions
        self.region_ids = np.arange(1,n_regions+1)

        # count pixels in each region
        areas = scipy.ndimage.measurements.sum(
            np.ones(labelled.shape),
            labels=labelled,
            index=self.region_ids
        ).astype(np.uint32)


        keep = areas > min_area

        coms = scipy.ndimage.measurements.center_of_mass(
            np.ones(labelled.shape),
            labels=labelled,
            index=self.region_ids[keep]
        )

        self.blobs = [
            Blob(color, *x) for x in zip(
                coms,
                areas[keep]
            )
        ]

    @property
    def debug_frame(self):
        # draw each region of the labelled image in a different hue
        import cv2

        frame = np.dstack((
            (self.labelled * 15) % 180,
            np.ones(self.labelled.shape) * 128,
            np.ones(self.labelled.shape) * 255
        )).astype(np.uint8)
        print(frame.shape)

        frame = cv2.cvtColor(frame, cv2.COLOR_HLS2BGR)
        return frame
