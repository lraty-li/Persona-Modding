targetStr = "属性攻击"

for char in targetStr:
    codePoint = char.encode("shiftjis")
    for code in codePoint:
        print(hex(code).replace("0x", ""), end=' ')
