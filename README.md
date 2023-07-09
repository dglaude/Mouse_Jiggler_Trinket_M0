# Mouse_Jiggler_Trinket_M0
Ultimate mouse jiggler that you enable or disable from your computer keyboard

A mouse jiggler is a device that generate tiny mouse mouvement on your computer to avoid it from going into sleep mode.
It is very easy to create a mouse jiggler with any CircuitPython microcontroler (that has a native USB port to do usb-hid.
But if here I want to create the ultimate mouse jiggler.

## Installation

Minimum installation only require the file `code.py` and a few libraries:
* `adafruit_hid` (folder)
* `adafruit_dotstar` (mpy file)
* `adafruit_pixelbuf` (mpy file)

If you want to customize the behaviour, you can add the file  `muconfig.py` and edit to uncomment some line and choose the value you want to use in place of the default.

If you want to us the Stealth mode you have to deploy the file `boot.py`, but be extremly carefull and have a wire handy to connect GPiO4 with Ground (Gnd) if you ever need to re-enable the mass storage in order to modify the code or parameter

## Usage



## Configuration

Without touching the code, there are a few way you can change the code behaviour by creating and editing the file `myconfig.py`:
```
RAINBOW = True           # Display a rainbow when active
RAINBOW_DELAY = 50       # Mouse movement occurs every 256*RAINBOW_DELAY ticks, that mean every rainbow rotation reach red.
AUTO_START = True        # Do you want jiggling to start automatically.
WARN_NO_USB = True       # Do you want high speed blinking LED when USB is not connected.
STEALTH_DEFAULT = False  # Do you want to hide the mass storage by default (short Gnd and 4 to reverse)
```
### RAINBOW

*Display a rainbow when active*

By default the jiggler navigate all the rainbow color when the mouse moving activity is enabled. If you want your mouse jiggler to be visually more discreet you can set **RAINBOW** to **False**. However that mean that the only way to know if the jiggler is active is to observer the mouse mouvement to figure out if it is active or not.

### RAINBOW_DELAY

*Mouse movement occurs every 256*RAINBOW_DELAY ticks, that mean every rainbow rotation reach red.*

...

### AUTO_START

*Do you want jiggling to start automatically.*

...

### WARN_NO_USB

*Do you want high speed blinking LED when USB is not connected.*

...

### STEALTH_DEFAULT

*Do you want to hide the mass storage by default (short Gnd and 4 to reverse)*

...

## Design decision

Requirement (feature wishlist):
1) Enable/Disable from keyboard
2) Works on Windows/Linux/Mac
3) Does not modify the computer behavior
4) Visual indication that it is activated or not
5) Stealth mode (no mass storage)
6) Small and cheap (target is to run on Trinked M0 board)
7) Recover from USB late connection and disconnection (power up, sleep, wake-up, ...)
8) User configurable (all option regrouped in a single file)

Initial idea to (1)enable/disable from keyboard has been to use the scrol lock key to enable and disable the jiggling.
This is possible because your computer send lock led status to all the keyboard connected, including your mouse jiggler.
However, the Scroll Lock does not exist on Mac(2), and on PC it (3)alter the computer behavior.
Also scroll lock (and numlock) is not always available on laptop keyboard.

So the solution is to use Caps Lock that is universally available, but it does (3)modify the computer behavior.
The trick is to use a kind of quick double click on the Caps Log key. This can be detected but the second click return to previous behavior.
And the Caps Lock key can keep it's normal behavior when you press it only one time (and not two time in a very short period of time).

For the visual indication(4), most Adafruit board have an RGB LED, either NeoPixel or DotStar like on the Trinked M0.
The choosen indication is to display a rainbow of colors, because everybody likes rainbow.

To permit (5)Stealth mode, it is possible to disable a lot of the USB feature by tweeking the boot.py file.
We can disable MIDI, Serial CDC and mass storage. Only keeping mouse for the jiggeling and keyboard for the caps lock led detection.
To be able to enable or disable Stealth mode you need a kind of jumper or button that you would press or close the circuit at startup time.
Since the Trinked has no such button, I soldered something on Ground and GPIO 4 (that are next to each other) and I can short that when needed.
You still have to decide if you want it default stealth on or off. Soldering might not be needed except to change the code.

The target is to use Trinket M0 to have a small and cheap solution (6), however, this require to work arround the limitation of the platform, do not acquire new M0 board, nowadays, a board based on RP2040 is much more powerfull and will work with this de

To recover from error, on can try to catch every possible exception, but since the code is small, forcing a restart 'on error'. This could also catch allocation memory error. In case of reboot, the current state (active or standby) can be lost. Because having the USB not connected could be the indication that the USB cable used does not contain data  a special warning indicator has been integrated.

Some parameter are available to customize the behaviour of the jiggler. They are all located in the optional myoptions.py file. If the file is not present or does not define some variable, the default value will be used.
