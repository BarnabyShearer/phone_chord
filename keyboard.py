#! /usr/bin/env python3

from brs001 import MOD, KEYS

PATERN = [
    set(),
    {4},
    {3},
    {3, 4},
    {2},
    {2, 4},
    {2, 3},
    {2, 3, 4},
]

BRAIL = PATERN + \
    [p | {8} for p in PATERN] + \
    [p | {7} for p in PATERN] + \
    [p | {7, 8} for p in PATERN] + \
    [p | {6} for p in PATERN] + \
    [p | {6, 8} for p in PATERN] + \
    [p | {6, 7} for p in PATERN] + \
    [p | {6, 7, 8} for p in PATERN] + \
    [p | {1} for p in PATERN] + \
    [p | {1, 8} for p in PATERN] + \
    [p | {1, 7} for p in PATERN] + \
    [p | {1, 7, 8} for p in PATERN] + \
    [p | {1, 6} for p in PATERN] + \
    [p | {1, 6, 8} for p in PATERN] + \
    [p | {1, 6, 7} for p in PATERN] + \
    [p | {1, 6, 7, 8} for p in PATERN] + \
    [p | {5} for p in PATERN] + \
    [p | {5, 8} for p in PATERN] + \
    [p | {5, 7} for p in PATERN] + \
    [p | {5, 7, 8} for p in PATERN] + \
    [p | {5, 6} for p in PATERN] + \
    [p | {5, 6, 8} for p in PATERN] + \
    [p | {5, 6, 7} for p in PATERN] + \
    [p | {5, 6, 7, 8} for p in PATERN] + \
    [p | {1, 5} for p in PATERN] + \
    [p | {1, 5, 8} for p in PATERN] + \
    [p | {1, 5, 7} for p in PATERN] + \
    [p | {1, 5, 7, 8} for p in PATERN] + \
    [p | {1, 5, 6} for p in PATERN] + \
    [p | {1, 5, 6, 8} for p in PATERN] + \
    [p | {1, 5, 6, 7} for p in PATERN] + \
    [p | {1, 5, 6, 7, 8} for p in PATERN] + \
    []

LAYOUT = [
    [
    '',
    'HID_KEY_ESCAPE',
    'HID_KEY_F1',
    'HID_KEY_F2',
    'HID_KEY_F3',
    'HID_KEY_F4',
    'HID_KEY_F5',
    'HID_KEY_F6',
    'HID_KEY_F7',
    'HID_KEY_F8',
    'HID_KEY_F9',
    'HID_KEY_F10',
    'HID_KEY_F11',
    'HID_KEY_F12',
    'HID_KEY_HOME',
    'HID_KEY_END',
    'HID_KEY_INSERT',
    'HID_KEY_DELETE',
    ], [
    '',
    'HID_KEY_GRAVE',
    'HID_KEY_1',
    'HID_KEY_2',
    'HID_KEY_3',
    'HID_KEY_4',
    'HID_KEY_5',
    'HID_KEY_6',
    'HID_KEY_7',
    'HID_KEY_8',
    'HID_KEY_9',
    'HID_KEY_0',
    'HID_KEY_MINUS',
    'HID_KEY_EQUAL',
    'HID_KEY_BACKSPACE',
    ], [
    ' ',
    'HID_KEY_TAB',
    'HID_KEY_Q',
    'HID_KEY_W',
    'HID_KEY_E',
    'HID_KEY_R',
    'HID_KEY_T',
    'HID_KEY_Y',
    'HID_KEY_U',
    'HID_KEY_I',
    'HID_KEY_O',
    'HID_KEY_P',
    'HID_KEY_BRACKET_LEFT',
    'HID_KEY_BRACKET_RIGHT',
    'HID_KEY_RETURN',
    ], [
    '  ',
    'HID_KEY_CAPS_LOCK',
    'HID_KEY_A',
    'HID_KEY_S',
    'HID_KEY_D',
    'HID_KEY_F',
    'HID_KEY_G',
    'HID_KEY_H',
    'HID_KEY_J',
    'HID_KEY_K',
    'HID_KEY_L',
    'HID_KEY_SEMICOLON',
    'HID_KEY_APOSTROPHE',
    'HID_KEY_BACKSLASH', # UK='#'
    ], [
    ' ',
    'KEYBOARD_MODIFIER_LEFTSHIFT',
    'HID_KEY_F3', # UK='\'
    'HID_KEY_Z',
    'HID_KEY_X',
    'HID_KEY_C',
    'HID_KEY_V',
    'HID_KEY_B',
    'HID_KEY_N',
    'HID_KEY_M',
    'HID_KEY_COMMA',
    'HID_KEY_PERIOD',
    'HID_KEY_SLASH',
    'KEYBOARD_MODIFIER_RIGHTSHIFT',
    ], [
    ' ',
    'FN',
    'KEYBOARD_MODIFIER_LEFTCTRL',
    'KEYBOARD_MODIFIER_LEFTGUI',
    'KEYBOARD_MODIFIER_LEFTALT',
    'HID_KEY_SPACE',
    'HID_KEY_SPACE',
    'HID_KEY_SPACE',
    'HID_KEY_SPACE',
    'HID_KEY_SPACE',
    'KEYBOARD_MODIFIER_RIGHTALT',
    'HID_KEY_PRINT_SCREEN',
    'KEYBOARD_MODIFIER_RIGHTCTRL',
    'HID_KEY_PAGE_UP',
    'HID_KEY_ARROW_UP',
    'HID_KEY_PAGE_DOWN',
    ],[
    ' ',
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    'HID_KEY_ARROW_LEFT',
    'HID_KEY_ARROW_DOWN',
    'HID_KEY_ARROW_RIGHT',
    ],
]

for row in LAYOUT:
    print(row[0], end="")
    for key in row[1:]:
        if key in {**KEYS, **MOD}:
            if len(key) == 9:
                print(key[-1], end="")
            else:
                print(" ", end="")
            print('\033[0;30;47m' + chr(0x2800 + BRAIL.index({**KEYS, **MOD}[key])) + '\033[0;97;40m', end=" ")
        elif key is None:
            print("  ", end=" ")
        else:
            print(" #", end=" ")
    print()
    print()
