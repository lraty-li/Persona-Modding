# 由tsv文件生成xlor

# DEBUG for seurapro 13_13


def getUnicodeList(
    tsvPath,
):
    unicodeList = []
    with open(tsvPath, "r") as tsvFile:
        for line in tsvFile.readlines():
            lastOfLine = False
            for char in line.split("\t"):
                if "\n" in char:
                    # last char of line
                    lastOfLine = True
                    char = char.replace("\n", "")
                if char == " ":
                    # 不知道3dsfont为什么导出的第一位是<sp/>，对应空格
                    unicodeList.append(f"<sp/> ")
                else:
                    charUnicodePoint = ord(char)
                    unicodeList.append(f"&#x{charUnicodePoint:04X}; ")
                if lastOfLine:
                    unicodeList.append(f"\n")
    return unicodeList


textMap = {
    "xlorPreText": """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE letter-order SYSTEM "letter-order.dtd">

<letter-order version="1.0">
	<head>
		<create user="" date="2014-12-09" />
		<title>seurapro_13_13.xlor</title>
		<comment></comment>
	</head>

	<body>
		<area width="16" />
		<order>
""",
    "xlorSubText": """		</order>
	</body>
</letter-order>
""",
    "xlltPreText": """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE letter-list SYSTEM "letter-list.dtd">

<letter-list version="1.0">
	<head>
		<create user="" date="2014-12-09" />
		<title>seurapro_13_13.xllt</title>
		<comment></comment>
	</head>

	<body>
		<letter>
""",
    "xlltSubText": """		</letter>
	</body>
</letter-list>""",
}


if __name__ == "__main__":
    sourceTsv = "./pq2_seurapro_13_13.tsv"
    outPutSubFixs = ["xlor", "xllt"]
    for opSubFix in outPutSubFixs:
        with open(sourceTsv + ".{}".format(opSubFix), "w+") as outputFile:
            preText = textMap["{}PreText".format(opSubFix)]
            subText = textMap["{}SubText".format(opSubFix)]
            outputFile.write(preText)
            dataList = getUnicodeList(sourceTsv)
            outputFile.write("".join(dataList))
            outputFile.write(subText)
            print()
