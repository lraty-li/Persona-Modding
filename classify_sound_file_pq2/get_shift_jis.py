targetStr = "準備中"

for char in targetStr:
    codePoint = char.encode("shiftjis")
    for code in codePoint:
        print(hex(code).replace("0x", ""), end=" ")
print()
targHexs = """
83 8A
"""
bBytes = bytes.fromhex(targHexs)
sstr = bBytes.decode("shiftjis")
sstrRev = "".join(list(reversed(sstr)))
print(sstr)
# print(sstrRev)
