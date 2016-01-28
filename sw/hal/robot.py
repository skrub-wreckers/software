from . import HardwareDevice, Arms, Drive, RegulatedDrive, ColorSensor, BreakBeams, DigitalIR, LimitSwitch
from tamproxy.devices import LongIR, DigitalInput
from .. import pins
from ..import constants


class Robot(HardwareDevice):
    def __init__(self, tamp):
        self.tamp = tamp
        self.arms = Arms(self.tamp)
        self.drive = RegulatedDrive(self.tamp)
        self.color_sensor = ColorSensor(self.tamp)

        self.left_long_ir = LongIR(self.tamp, pins.l_ir_long)
        self.right_long_ir = LongIR(self.tamp, pins.r_ir_long)

        self.left_short_ir = DigitalIR(self.tamp, pins.l_ir_short)
        self.right_short_ir = DigitalIR(self.tamp, pins.r_ir_short)
        
        self.left_bumper = LimitSwitch(self.tamp, pins.l_bumper, pullup = True)
        self.right_bumper = LimitSwitch(self.tamp, pins.r_bumper, pullup = True)

        self.break_beams = BreakBeams(self.tamp)
        
        self.time_remaining = constants.round_time
