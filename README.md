# Mouse_Jiggler_Trinket_M0
Ultimate mouse jiggler that you enable or disable from your computer keyboard

A mouse jiggler is a device that generate tiny mouse mouvement on your computer to avoid it from going into sleep mode.
It is very easy to create a mouse jiggler with any CircuitPython microcontroler (that has a native USB port to do usb-hid.
But if here I want to create the ultimate mouse jiggler.

Requirement (feature wishlist):
1) Enable/Disable from keyboard
2) Works on Windows/Linux/Mac
3) Does not modify the computer behavior
4) Visual indication that it is activated or not
5) (optional) Stealth mode
6) Small and cheap (target is to run on Trinked M0 board)
7) (not done yet) Must survive and continue to work if powered without the computer started
8) (not done yet) Must survive and continue to work when the the computer is powed off then on


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

...


