\
├─2D8AE9E086F548C89DD1D93A22D272AC
    ├─68A8F400A4EC461C9E4A863A14D948C3 (2KB)
    ├─container.205
├─156997FC78674F96A11004B4225208E2
    ├─C45B7F3841954E67A870C066E5E6074F (16KB)
    ├─container.1
...

SYSTEM.DAT文件会相对一般的存档文件DATA.DAT小很多，另外container文件也能够区分，用二进制读取即可看到


The SYSTEM.DAT file will be much smaller than the general game save file DATA.DAT. And the container file can also be distinguished by reading it in binary.


container.205:
0000h  04 00 00 00 01 00 00 00 53 00 59 00 53 00 54 00  ........S.Y.S.T. 
0010h  45 00 4D 00 2E 00 44 00 41 00 54 00 00 00 00 00  E.M...D.A.T..... 

container.1:
0000h  04 00 00 00 01 00 00 00 44 00 41 00 54 00 41 00  ........D.A.T.A. 
0010h  2E 00 44 00 41 00 54 00 00 00 00 00 00 00 00 00  ..D.A.T......... 
