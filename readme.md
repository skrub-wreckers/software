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
![https://i.imgur.com/2weGAwh.png](https://i.imgur.com/2weGAwh.png)

### Subsumption

Uses the `asyncio` module (or rather its python 2 backport, `trollius`)
