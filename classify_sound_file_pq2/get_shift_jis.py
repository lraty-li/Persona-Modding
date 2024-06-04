targetStr = "区画"

for char in targetStr:
    codePoint = char.encode("shiftjis")
    for code in codePoint:
        print(hex(code).replace("0x", ""), end=" ")
print()
targHexs = """
00 00 00 00 89 66 93 6C 00 00 00 00 89 6C 93 6C
00 00 00 00 8F 74 93 6C 00 00 00 00 97 79 93 6C
00 00 00 00 97 7A 93 6C 00 00 00 00 8C 8B 93 6C

"""
bBytes = bytes.fromhex(targHexs)
sstr = bBytes.decode("shiftjis")
sstrRev = "".join(list(reversed(sstr)))
print(sstr)
# print(sstrRev)
