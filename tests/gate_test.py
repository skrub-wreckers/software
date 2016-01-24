from tamproxy.devices import *
from tamproxy import TAMProxy
import time
from sw.gui import Window

if __name__ == "__main__":
    with TAMProxy() as tamp:
        led = DigitalOutput(tamp, 0)
        reading = DigitalInput(tamp, 15)
        w = Window(500, [])

        led_on = True

        while True:
            print led_on, reading.val
            time.sleep(0.1)

            try:
                c = w.keys.get_nowait()
                if c == ' ':
                    led_on = not led_on
                    led.write(not led_on)
            except:
                pass