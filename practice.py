#! /usr/bin/env python3

from threading import Timer
import evdev
import time

from brs001 import MOD, KEYS
MOD = {v:k for k, v in MOD.items()}
KEYS = {v:k for k, v in KEYS.items()}

INPUT = {
    30: 1,
    31: 2,
    32: 3,
    33: 4,
    36: 8,
    37: 7,
    38: 6,
    39: 5
}

GRACE = 0.100

dev = evdev.InputDevice('/dev/input/by-path/platform-i8042-serio-0-event-kbd')
dev.grab()
dev.repeat = evdev.device.KbdInfo(repeat=0, delay=99999) #often ignored

mods = set()

def done():
    pressed = set()
    for key in dev.active_keys():
        pressed.add(INPUT[key])
    pressed = frozenset(pressed)
    if pressed in MOD:
        if MOD[pressed] in mods:
            mods.remove(MOD[pressed])
        else:
            mods.add(MOD[pressed])
        return
    print(KEYS.get(pressed, None), mods)

timer = None
for event in dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        keyevent = evdev.categorize(event)
        if keyevent.keystate == keyevent.key_hold:
            continue
        if timer is not None:
            timer.cancel()
        timer = Timer(GRACE, done)
        timer.start()
        if keyevent.scancode == evdev.ecodes.KEY_ESC:
            break
dev.ungrab()
