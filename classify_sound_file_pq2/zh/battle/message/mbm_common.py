HEX_F8_VALUE = b"\xf8"[0]
HEX_7F_VALUE = b"\x7F"[0]
HEX_FF_VALUE = b"\xff"[0]


HEADER_SIZE = 0x20
MSG_COUNT_OFFSET = 0x10
MSG_INFO_SIZE = 0x10
MSG_NO_OFFSET = 0x0
MSG_SIZE_OFFSET = 0x4
MSG_OFFSET = 0x8
FILE_SIZE_OFFSET = 0xC

MBM_HEADER_TEMPLATE = "00 00 00 00 4D 53 47 32 00 00 01 00 84 03 00 00 1E 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00"
MBM_MSG_INFO_TEMPLATE = "00 00 00 00 0E 00 00 00 00 02 00 00 00 00 00 00"