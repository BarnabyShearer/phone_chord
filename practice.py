#! /usr/bin/env python3

from threading import Timer
import evdev
import time

from brs001 import MOD, KEYS
MOD = {v:k for k, v in MOD.items()}
KEYS = {v:k for k, v in KEYS.items()}

import keyboard

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

GRACE = 0.070

dev = evdev.InputDevice('/dev/input/by-path/platform-i8042-serio-0-event-kbd')
dev.grab()
dev.repeat = evdev.device.KbdInfo(repeat=0, delay=99999) #often ignored

ui = evdev.UInput()
mods = set()
held = set()

def hid2key(key):
    return evdev.ecodes.ecodes[
        key.replace(
            "HID_KEY_",
            "KEY_"
        ).replace(
            "KEYBOARD_MODIFIER_",
            "KEY_"
        ).replace(
            "KEY_PERIOD",
            "KEY_DOT"
        ).replace(
            "KEY_RETURN",
            "KEY_ENTER"
        ).replace(
            "GUI",
            "META"
        ).replace(
            "ARROW_",
            ""
        ).replace(
            "PAGE_",
            "PAGE"
        ).replace(
            "ESCAPE",
            "ESC"
        ).replace(
            "BRACKET_LEFT",
            "LEFTBRACE"
        ).replace(
            "BRACKET_RIGHT",
            "RIGHTBRACE"
        )
    ]

def done():
    global held
    pressed = set()
    for key in dev.active_keys():
        if key in INPUT:
            pressed.add(INPUT[key])
    pressed = frozenset(pressed)
    if pressed in MOD:
        if MOD[pressed] in mods:
            mods.remove(MOD[pressed])
            ui.write(evdev.ecodes.EV_KEY, hid2key(MOD[pressed]), 0)
        else:
            mods.add(MOD[pressed])
            ui.write(evdev.ecodes.EV_KEY, hid2key(MOD[pressed]), 1)
        return
    if pressed in KEYS:
        if KEYS[pressed] not in held:
            held.add(KEYS[pressed])
            ui.write(evdev.ecodes.EV_KEY, hid2key(KEYS[pressed]), 1)
    else:
        for key in held:
            ui.write(evdev.ecodes.EV_KEY, hid2key(key), 0)
        held = set()
    ui.syn()
    #print(KEYS.get(pressed, None), mods)

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
