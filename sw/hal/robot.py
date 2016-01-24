from . import HardwareDevice, Arms, Drive, RegulatedDrive, ColorSensor
from tamproxy.devices import LongIR, ShortIR
from .. import pins


class Robot(HardwareDevice):
    def __init__(self, tamp):
        self.tamp = tamp
        self.arms = Arms(self.tamp)
        self.drive = Drive(self.tamp)
        self.color_sensor = ColorSensor(self.tamp)

        self.left_long_ir = LongIR(self.tamp, pins.l_ir_long)
        self.right_long_ir = LongIR(self.tamp, pins.r_ir_long)

        self.left_short_ir = ShortIR(self.tamp, pins.l_ir_short)
        self.right_short_ir = ShortIR(self.tamp, pins.r_ir_short)
        self.back_short_ir = ShortIR(self.tamp, pins.b_ir_short)
