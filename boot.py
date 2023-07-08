STEALTH_DEFAULT = False  # Do you want to hide the mass storage by default (short Gnd and 4 to reverse)

try:
    from myconfig import *
except ImportError:
    pass

import storage, usb_cdc
import board, digitalio
import usb_hid, usb_midi

button = digitalio.DigitalInOut(board.D4)
button.pull = digitalio.Pull.UP

# Disable devices only if button is not pressed.
if button.value == STEALTH_DEFAULT:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((usb_hid.Device.MOUSE,usb_hid.Device.KEYBOARD))       # Enable just MOUSE and KEYBOARD.
