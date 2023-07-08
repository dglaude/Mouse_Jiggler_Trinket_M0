import supervisor
supervisor.set_next_code_file(None, reload_on_success=True, reload_on_error=True)
supervisor.set_next_code_file(None, reload_on_error=True)

RAINBOW = True           # Display a rainbow when active
RAINBOW_DELAY = 100      # Mouse movement occurs every 256*RAINBOW_DELAY ticks, that mean every rainbow rotation reach red.
AUTO_START = False       # Do you want jiggling to start automatically.
WARN_NO_USB = False      # Do you want high speed blinking LED when USB is not connected.

try:
    from myconfig import *
except ImportError:
    pass

import board
import digitalio
#import time
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from rainbowio import colorwheel
import adafruit_dotstar

# Start of code from: https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html
_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff
# End of code from: https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html

RAINBOW_DELAY = 50 # Mouse movement occurs every 256*RAINBOW_DELAY ticks, that mean every rainbow rotation reach red.
last = supervisor.ticks_ms()
color_time = last

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()
led.value = False

if WARN_NO_USB:
    while not supervisor.runtime.usb_connected:
        last = supervisor.ticks_ms()
        if ticks_diff (last, color_time) > RAINBOW_DELAY:
            color_time = last
            led.value = not led.value
    led.value = False

num_pixels = 1
pixels = adafruit_dotstar.DotStar(board.DOTSTAR_CLOCK, board.DOTSTAR_DATA, num_pixels, brightness=0.1, auto_write=False)
rc_index = 0

octogonal_direction = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
iterator = iter(octogonal_direction)
distance=2

active = False
jiggle = AUTO_START

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

raise_flag = False
new_caps = kbd.led_on(Keyboard.LED_CAPS_LOCK)

while True:
    last = supervisor.ticks_ms()

    old_caps = new_caps
    new_caps = kbd.led_on(Keyboard.LED_CAPS_LOCK)

    if new_caps and not old_caps:
        raise_time = last
        raise_flag = True
        led.value = True

    if raise_flag:
        since_when = ticks_diff (last, raise_time)
        if ticks_diff (last, raise_time) > 1000:
            raise_flag = False
            led.value = False
        else:
            if not new_caps:
                jiggle = not jiggle
                color_time = last
                if not jiggle:
                    pixels[0] = (0,0,0)
                    pixels.show()
                raise_flag = False
                led.value = False

    if jiggle:
        if ticks_diff (last, color_time) > RAINBOW_DELAY:
            color_time = last
            rc_index = (rc_index + 1) & 255
            pixels[0] = colorwheel(rc_index)
            if RAINBOW:
                pixels.show()
            if rc_index == 0:
                try:
                    element = next(iterator)
                except StopIteration:
                    iterator = iter(octogonal_direction)
                    element = next(iterator)
                mouse.move(x=distance*element[0], y=distance*element[1])

