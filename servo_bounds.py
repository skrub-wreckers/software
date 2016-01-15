from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Servo


class ServoWrite(Sketch):
    """Cycles a servo back and forth between 1050us and 1950us pulse widths (most servos are 1000-2000)"""

    def setup(self):
        self.servo = Servo(self.tamp, 10)
        self.servo.write(2200)
        self.timer = Timer()
        self.val = 2200

    def loop(self):
        raw_input()
        self.val += 10
        print self.val
        self.servo.write(self.val)

if __name__ == "__main__":
    sketch = ServoWrite()
    sketch.run()
