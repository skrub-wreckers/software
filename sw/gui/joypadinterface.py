import ctypes
import math
import time
import pygame

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_4  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint


class JoystickInterface(object):
    def __init__(self, joy=None):
    	if joy is None:
			joy = pygame.joystick.Joystick(0)
    	joy.init()
        self.joy = joy

    @property
    def move_cmd(self):
        return (-self.joy.get_axis(1), -self.joy.get_axis(0))

    @property
    def left_arm(self):
        return self.joy.get_button(4)

    @property
    def right_arm(self):
        return self.joy.get_button(5)

    @property
    def open_silo(self):
        return self.joy.get_button(3)

    @property
    def close_silo(self):
        return self.joy.get_button(0)

    def set_bumpers(self, left, right):
    	amt = 32767
        vibration = XINPUT_VIBRATION(left * amt, right * amt)
    	XInputSetState(self.joy.get_id(), ctypes.byref(vibration))
