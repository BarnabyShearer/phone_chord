#! /usr/bin/env python3

from brs001 import MOD, KEYS

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
