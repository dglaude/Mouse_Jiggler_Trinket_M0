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

This control how frequently the mouse is moved, and it is moved every 256 color change in the rainbow animation (even if you don't enable it).
The same delay is used for fast blinking (attract mode) when USB is not connected.
You may want to tune this setting depending on how fast your computer goes to sleep or detect innactivity, and how disturbing it is to have the mouse moving when you use it.

### AUTO_START

*Do you want jiggling to start automatically.*

You can have the jiggling start automatically as soon as USB is detected. This is usefull if you permanently plug the jiggler into your computer (maybe pick a port that is not powered when your computer is powered off.
If you don't enable auto-start, you will have to double click CAPS_LOCK everytime you want to enable it.

### WARN_NO_USB

*Do you want high speed blinking LED when USB is not connected.*

If you don't use a USB Data cable, or if there is a problem and your computer does not connect with the mouse jiggler, the red LED from the board will blink quickly. This could also be the behaviour when you put your computer to sleep, but the mouse jiggler is connected to an always powered USB port.
If you don't want that warning or find the fastly blinking LED disturbing, you can disable that warning.

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

## Making the software work on more M0 devices

Reminder, you should avoid M0 / Samd21 devices as they have a lot of limitation and do not support any of the new tricks that CircuitPython can do... there is just not enough space for the code, nor memory for holding a full core. This comment does not apply to Raspberry Pico / RP2040, those board are M0 or M0+ but have a lot of memory and most of the time a big flash attached to it.

The question is to see if we can run on other constrained platform and what changes are needed. And at one point I will have to change this repository name to not be specific to the Trinket.

### SeedStudio Xiao 

Normal firmware: https://circuitpython.org/board/seeeduino_xiao/
Keyboard optimized firmware: https://circuitpython.org/board/seeeduino_xiao_kb/ (same hardware different selection of modules)

The original Xiao does not have an RGB LED, it only has two LED, the green "powered" and the orange that is controlable.
Also there are no button, not even the reset button, so it can be very simple and robust (while harder to do the initial setup or firwmare upgrade).

So the code will have to replace the rainbow part by some LED way to warn the user, I think PWM out the LED to have something that is of variable light intensity would have the best effect, and we can keep the high speed blinking for alert mode when no USB is connected.

### Original QT Py

Product page: https://www.adafruit.com/product/4600
Firmware: https://circuitpython.org/board/qtpy_m0/

The original QT Py does not have an LED, but just that RGB NeoPixel, and that is NeoPixel, not DotStar like on the Trinket M0.

So the code will need to be adapted so that it works with NeoPixel, and the fast blinking of the LED will have to be done with the NeoPixel too.

