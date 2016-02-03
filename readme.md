Installation
------------

```
git clone https://github.com/skrub-wreckers/TAMProxy-pyHost.git
pip install -e TAMProxy-pyHost
git clone https://github.com/skrub-wreckers/software.git
cd software
pip install -e .
```

Which then exposes a `sw` package for all the tests to use

Note that the `python-opencv` and `pygame` packages are not on PyPI, so will have to found elsewhere


### Windows
On windows, all the needed [wheel packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/) can be found online:

 * opencv-python
 * scipy
 * numpy
 * pygame

After installing these, try pip again

Implementation details
----------------------

### Vision
#### Color partitioning
![https://i.imgur.com/2weGAwh.png](https://i.imgur.com/2weGAwh.png)
#### Blob detection
Done using the `scipy.ndimage` tools to find continuous regions of the image
Pixels above the first chunk of blue pixels from the bottom of the image are ignored
#### Spacial mapping
Pixel locations are mapped to world space by finding the camera matrix, assuming no lens distortion, and that a random guy on the internet measured the FOV correctly. Using this matrix, a pixel can be projected onto any plane in robot space - we mostly project onto the plane z = 1 inch.

### Subsumption

Uses the `asyncio` module (or rather its python 2 backport, `trollius`). This let us run and cancel small tasks in a predictable and threadsafe (by means of not using threads at all).

Our task priority, from low to high, consisted roughly of:

 * Spin 360, then drive straight forever
 * Drive or turn towards a cube if one is seen
 * Bounce off walls, using the bumpers and IR
 * Stop and pick up cubes if we're pushing any
