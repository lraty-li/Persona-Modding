filepath = r'f:\TMP\cpk_output_workplace\ori-data\battle\table\personanametable.tbl'

def printBytes(bBytes):
    for bByte in bBytes:
        print("{:02x}".format(bByte), end=" ")
    print("")
    

data = []
print()
print()
with open(filepath, 'rb') as file:
    data = file.read(2)
    printBytes(data)
    data = file.read(48)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(48)
    printBytes(data)
    data = file.read(50)
    printBytes(data)
    data = file.read(48)
    printBytes(data)
    data = file.read(50)
    printBytes(data)
    data = file.read(48)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(44)
    printBytes(data)
    data = file.read(52)
    printBytes(data)
    data = file.read(56)
    printBytes(data)
    data = file.read(46)
    printBytes(data)
    data = file.read(48)
    printBytes(data)
    data = file.read(34)
    printBytes(data)
    # message
    # data = file.read(0xb)
    # print(data.decode('shiftjis'))
    # data = file.read(0x9)
    # print(data.decode('shiftjis'))
    # data = file.read(0x9)
    # print(data.decode('shiftjis'))
    # data = file.read(0xd)
    # print(data.decode('shiftjis'))
    strBytes = []
    data = file.read(1)
    strBytes.append(data)
    while(len(data) == 1):
        if(data != b'\x00'):
            strBytes.append(data)
        else:
            print(b''.join(strBytes).decode('shiftjis'))
            strBytes = []
        data = file.read(1)
print()