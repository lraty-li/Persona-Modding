@REM 提取cci
.\3dstool.exe -xvt01234567f cci cci\0.cxi cci\1.cfa cci\2.cfa cci\3.cfa cci\4.cfa cci\5.cfa cci\6.cfa cci\7.cfa .\pq2.3ds --header .\cci\ncsdheader.bin

@REM 仅提取0.cxi
.\3dstool.exe -xvt0f cci cci\0.cxi .\pq2.3ds --header .\cci\ncsdheader.bin

@提取 0.cxi内容
.\3dstool.exe -xvtf cxi cci\0.cxi --header cci\cxi0\ncchheader.bin --exh cci\cxi0\exh.bin --logo cci\cxi0\logo.bcma.lz --plain cci\cxi0\plain.bin --exefs cci\cxi0\exefs.bin --romfs cci\cxi0\romfs.bin --key0

@REM 提取exefs
.\3dstool.exe -xvtfu exefs cci\cxi0\exefs.bin --exefs-dir cci\cxi0\exefs --header cci\cxi0\exefs\exefsheader.bin

@REM 提取romfs
.\3dstool.exe -xvtf romfs cci\cxi0\romfs.bin --romfs-dir cci\cxi0\romfs