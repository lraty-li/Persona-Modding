targetStr = "追加"

for char in targetStr:
    codePoint = char.encode("shiftjis")
    for code in codePoint:
        print(hex(code).replace("0x", ""), end=" ")
print()
print()
print()
targHexs = """
ff ff

"""
bBytes = bytes.fromhex(targHexs)
sstr = bBytes.decode("shiftjis")
sstrRev = "".join(list(reversed(sstr)))
print(sstr)
# print(sstrRev)
