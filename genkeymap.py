#! /usr/bin/env python3

MOD = {
    'KEYBOARD_MODIFIER_LEFTCTRL': {3, 7},
    'KEYBOARD_MODIFIER_LEFTSHIFT': {2, 6},
    'KEYBOARD_MODIFIER_LEFTALT': {4, 8},
    'KEYBOARD_MODIFIER_LEFTGUI': {2, 3, 4, 7, 8},
    #'KEYBOARD_MODIFIER_RIGHTCTRL': {},
    #'KEYBOARD_MODIFIER_RIGHTSHIFT': {},
    'KEYBOARD_MODIFIER_RIGHTALT': {4, 7, 8},
    'KEYBOARD_MODIFIER_RIGHTGUI': {3, 4, 6, 7, 8},
}

#{6, 7}, and {7, 8} are very good spare
#{1, 2}, and {2, 3} are reserved for number and arrow chords

KEYS = {
    'HID_KEY_ESCAPE': {3, 4},
    #'HID_KEY_F1': {},
    #'HID_KEY_F2': {},
    #'HID_KEY_F3': {},
    #'HID_KEY_F4': {},
    #'HID_KEY_F5': {},
    #'HID_KEY_F6': {},
    #'HID_KEY_F7': {},
    #'HID_KEY_F8': {},
    #'HID_KEY_F9': {},
    #'HID_KEY_F10': {},
    #'HID_KEY_F11': {},
    #'HID_KEY_F12': {},
    'HID_KEY_HOME': {1, 2, 3},
    'HID_KEY_END': {5, 6, 7},
    'HID_KEY_INSERT': {6, 7, 8},
    'HID_KEY_DELETE': {2, 3, 4},

    'HID_KEY_GRAVE': {1, 2, 5, 7, 8},
    'HID_KEY_1': {1, 2, 5},
    'HID_KEY_2': {1, 2, 6},
    'HID_KEY_3': {1, 2, 5, 6},
    'HID_KEY_4': {1, 2, 7},
    'HID_KEY_5': {1, 2, 5, 7},
    'HID_KEY_6': {1, 2, 6, 7},
    'HID_KEY_7': {1, 2, 5, 6, 7},
    'HID_KEY_8': {1, 2, 8},
    'HID_KEY_9': {1, 2, 5, 8},
    'HID_KEY_0': {1, 2, 6, 8},
    'HID_KEY_MINUS': {1, 2, 5, 6, 8},
    'HID_KEY_EQUAL': {1, 2, 7, 8},
    'HID_KEY_BACKSPACE': {8},

    'HID_KEY_TAB': {1, 2, 3, 4},
    'HID_KEY_Q': {3, 4, 5},
    'HID_KEY_W': {2, 7},
    'HID_KEY_E': {2},
    'HID_KEY_R': {2, 5},
    'HID_KEY_T': {5},
    'HID_KEY_Y': {2, 8},
    'HID_KEY_U': {4, 5},
    'HID_KEY_I': {3},
    'HID_KEY_O': {4},
    'HID_KEY_P': {3, 8},
    'HID_KEY_BRACKET_LEFT': {1, 2, 3, 4, 5, 8},
    'HID_KEY_BRACKET_RIGHT': {1, 4, 5, 6, 7, 8},
    'HID_KEY_RETURN': {5, 6, 7, 8},

    #'HID_KEY_CAPS_LOCK': {},
    'HID_KEY_A': {1},
    'HID_KEY_S': {7},
    'HID_KEY_D': {1, 6},
    'HID_KEY_F': {4, 7},
    'HID_KEY_G': {1, 8},
    'HID_KEY_H': {3, 5},
    'HID_KEY_J': {2, 4},
    'HID_KEY_K': {1, 4},
    'HID_KEY_L': {3, 6},
    'HID_KEY_SEMICOLON': {2, 3, 5, 6, 7, 8},
    'HID_KEY_APOSTROPHE': {3, 5, 6, 7, 8},
    'HID_KEY_BACKSLASH': {1, 2, 3, 4, 5, 6, 7, 8}, # UK='#'

    #'HID_KEY_SHIFT_LEFT': {},
    'HID_KEY_F3': {5, 1, 2, 3, 4}, # UK='\'
    'HID_KEY_Z': {5, 7},
    'HID_KEY_X': {8, 5},
    'HID_KEY_C': {4, 6},
    'HID_KEY_V': {8, 6},
    'HID_KEY_B': {1, 3},
    'HID_KEY_N': {6},
    'HID_KEY_M': {1, 7},
    'HID_KEY_COMMA': {5, 6, 8},
    'HID_KEY_PERIOD': {5, 6},
    'HID_KEY_SLASH': {1, 5, 6, 7, 8},
    #'HID_KEY_SHIFT_RIGHT': {},

    #'HID_KEY_CONTROL_LEFT': {},
    #'HID_KEY_GUI_LEFT': {},
    #'HID_KEY_ALT_LEFT': {},
    'HID_KEY_SPACE': {1, 5},
    #'HID_KEY_ALT_RIGHT': {},
    #'HID_KEY_PRINT_SCREEN': {},
    #'HID_KEY_CONTROL_RIGHT': {},
    'HID_KEY_PAGE_UP': {2, 3, 7, 8},
    'HID_KEY_ARROW_UP': {2, 3, 8},
    'HID_KEY_PAGE_DOWN': {2, 3, 5, 6},
    'HID_KEY_ARROW_LEFT': {2, 3, 7},
    'HID_KEY_ARROW_DOWN': {2, 3, 5},
    'HID_KEY_ARROW_RIGHT': {2, 3, 6}

    #'HID_KEY_GUI_RIGHT': {},
    #'HID_KEY_APPLICATION': {},
    #'HID_KEY_EUROPE_1': {},
    #'HID_KEY_EUROPE_2': {}
    #'HID_KEY_SCROLL_LOCK': {},
    #'HID_KEY_NUM_LOCK': {},
    #'HID_KEY_PAUSE': {},
    #'HID_KEY_POWER': {},
    #F13-15, KEYPAD_*
    #Media controls, power controls, app launch, browser
}

# Freeze (so we can hash)
for k, v in MOD.items():
    MOD[k] = frozenset(v)
for k, v in KEYS.items():
    KEYS[k] = frozenset(v)

def toint(keys):
    key = 0
    for i in range(1, 9):
        if i in keys:
            key |= 1 << (i-1)
    return key

def fromint(key):
    keys = set()
    for i in range(8):
        if key & (1 << i):
            keys.add(i + 1)
    return keys

def totable(name, keys):
    buf = ""
    keys = {toint(v): k for k, v in keys.items()}
    keys[0] = '0'
    buf += "uint8_t %s[] = {\n" % name
    for x in range(32):
        buf += "    "
        for y in range(8):
            buf += keys.get(8*x + y, '0')
            if not y == 7:
                buf += ", "
        buf += ",\n"
    buf += "};\n"
    return buf

# Check dupes
seen = set()

for k, v in MOD.items() | KEYS.items():
    if toint(v) in seen:
        print("Dupe Key:", k, v)
    seen.add(toint(v))

# Check unused 1, 2, 3 chords
good = set()
for x in range(1, 9):
    good.add(toint({x}))
    for y in range(1, 9):
        good.add(toint({x, y}))
        for z in range(1,9):
            good.add(toint({x, y, z}))

#for x in good - seen:
#    print(fromint(x))

#print table
print(totable("modifiers", MOD))
print(totable("hidcode", KEYS))
