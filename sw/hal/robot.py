from . import HardwareDevice, Arms, Drive, RegulatedDrive, ColorSensor

class Robot(HardwareDevice):
    def __init__(self, tamp):
        self.tamp = tamp
        self.arms = Arms(self.tamp)
        self.drive = Drive(self.tamp)
        self.color_sensor = ColorSensor(self.tamp)
