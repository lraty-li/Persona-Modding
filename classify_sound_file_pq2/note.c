3dstool 解包3ds


https://github.com/dnasdw/3dsfont






/* Cue List (Cue ID) */
#define CRI_E400510_E400510_001_0081     (   1) /* お父さん…！お父さん、お、父さん…！  */

001:编号
0081：speaker，在common_acf.h、btl_voice.h中可以找到对应人名
0081:ひかり
event里的语音倒是能对应

#define CRI_E400510_E400510_119_0022     ( 119) /* そうだよ。女の子を泣かせるようなことはしないよね？　ジョーカー？  */
#define CRI_XRD760_ACF_CATEGORY_22               (41) /* btl_voice/22 //高巻杏 */
22表示高巻杏



bgm:
#define CRI_BGM_EVENT03       ( 303) /* キミの記憶 - PSQ2 ver  */
00034_streaming.adx

#define CRI_BGM_EVENT04       ( 304) /* 記憶の片隅 - PSQ2 ver  */
00035_streaming.adx




pq2_seurapro_13_13 比 pq2_seurapro_12_12 在12行多了一个∥，之后全部往后推






https://github.com/Meloman19/PersonaEditor/blob/master/how_encoded_text.jpg
未定义：
出现了high, low surrague 130,79的字符

/// <summary>
/// Offset from start of glyph range to start of the char table.
/// </summary>
private const int CHAR_TO_GLYPH_INDEX_OFFSET = 0x60;

/// <summary>
/// Size of a single glyph table.
/// </summary>
private const int GLYPH_TABLE_SIZE = 0x80;

/// <summary>
/// The high bit serves as a marker for a table index.
/// </summary>
private const int GLYPH_TABLE_INDEX_MARKER = 0x80;

// add extended characters, and make sure to include the ascii range again due to overlap
for (int charIndex = 0x20; charIndex < charTable.Count; charIndex++)
{
    int glyphIndex = charIndex + CHAR_TO_GLYPH_INDEX_OFFSET;
    int tableIndex = (glyphIndex / GLYPH_TABLE_SIZE) - 1;
    int tableRelativeIndex = glyphIndex - (tableIndex * GLYPH_TABLE_SIZE);

    mCodePointToChar[new CodePoint((byte)(GLYPH_TABLE_INDEX_MARKER | tableIndex), (byte)(tableRelativeIndex))] = charTable[charIndex];
}

https://github.com/Meloman19/PersonaEditor/issues/32

Surrogate to index
highSurrogate
GLYPH_TABLE_INDEX_MARKER | tableIndex
tableIndex 2 或者 130
glyphIndex=tableIndex +1 * 0x80
charIndex =  tableIndex +1 * 0x80 - 0x60
charIndex 34 或者 162

lowSurrogate :
glyphIndex - (tableIndex * GLYPH_TABLE_SIZE);
int(charIndex + CHAR_TO_GLYPH_INDEX_OFFSET) - (int((glyphIndex / GLYPH_TABLE_SIZE) - 1) * GLYPH_TABLE_SIZE)
int(charIndex + CHAR_TO_GLYPH_INDEX_OFFSET) - (int((int(charIndex + CHAR_TO_GLYPH_INDEX_OFFSET) / GLYPH_TABLE_SIZE) - 1) * GLYPH_TABLE_SIZE)

lowSurrogate>=96
79非法


https://discord.com/channels/746211612981198989/746230710150496367/1208661109028954113
just use -Encoding SJ
https://zh.wikipedia.org/wiki/Shift_JIS
https://learn.microsoft.com/en-us/dotnet/api/system.text.encoding?view=net-8.0



https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/International-Character-Set-Support/Japanese-Encodings-and-Mapping-Standards

https://blog.csdn.net/dietime1943/article/details/60577428

http://www.k73.com/3ds/120266.html

F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe D:\code\git\Persona-Modding\classify_sound_file_pq2\tmp\e000_015.bf.flow D:\code\git\Persona-Modding\classify_sound_file_pq2\tmp\e000_015.bf.msg D:\code\git\Persona-Modding\classify_sound_file_pq2\tmp\e000_015.bf.msg.h -Compile -OutFormat V2 -Library pq2 -Encoding SJ
F:\modding\persona-tools\Atlus-Script-Tools\AtlusScriptCompiler.exe .\e000_015.bf.flow.bf --Decompile -Library pq2 -Encoding SJ

问题：
如何让打包使用我修改过的的字符集（中文的shift jis），而不是经过偏移的的tsv或者cp932
改compiler exe，新建一种encoding类型？


private bool TryCompileImpl( MessageScriptParser.CompilationUnitContext context, out MessageScript script )

        private void ProcessTextToken( StringToken token, List<byte> bytes )

dialogContexts 就是msg里每一段/块，比如e000_015.bf.msg有14块

Window 对话场景
page 每一“句”话，一行台词

似乎p345的字库其实也是shift jis的改版，看起来内置了ASCII范围，然后字符偏移到0x80开始

转换回bcfnt的时候是怎么确保编码的呢？
charset txt 只是保存字符
xlor: letter order
xllt : letter filter? 记录有哪些字符 "限制生成bcfnt文件中的字符"
位图信息还是存在bcfnt里。

https://uic.io/zh/charset/compare/shift_jis/cp932/
compliler 实际上用的是cp932解包出来，汉字方面编码是一致的

为什么都会有个0x40的间隔？
88F0	芋	鰯	允	印	咽	員	因	姻	引	飲	淫	胤	蔭				
8940	院	陰	隠	韻	吋	右	宇	烏	羽	迂	雨	卯	鵜	窺	丑	碓	
TODO 列出原本p345 tsv的编码范围，如果都是一样的有间隔之类的，也许不用改多少
只要确保bcfnt跟编译回去的bf文件用的是同一套字库就行？3ds取字有没有什么范围问题？

0: 游戏如何调用对应字符？这个编码规律应该不是内置的，只要读到数据就按数据找
1: 编译器: 
希望在原本的encoding基础上另外支持pq系列的自定义字符
如何编排？
在兼容原日文的同时，新增中文？免得没汉化的地方乱码：只换掉原本汉字的地方 shift jis 0x8890

2: 字库

打包回游戏文件
tsv -> bcfnt

游戏还是按shift jis索引文字，所以要做的是生成虚假的bmp，但编码回bcfnt的时候用的还是“日文的xlor跟xllt”
所谓的编码关系也许并不是位置体现，而是某shift jis对应某图片？
那么tsv编码出bf的时候，其编码要与shift jis一致： 某中文->对应的日文->shift jis code

流程：
字库侧：
汉化tsv，原日文tsv，两者除了具体字不一样外，内部字符数字等一样
汉化tsv 生成 bmp
日文tsv 生成xllt xlor
至此，日文tsv中的日文能够对应bmp对应位置的中文位图

bf编码：
需要某个字->对应的日文->对应的shift jis 码
例如中文 “你” 对应 日文“亜”，编码完成后，bf文件中实际存在的“你”对应的代码是 0x889F(亜的 shift jis编码)
对汉化流程来说：写一个py脚本，自动替换掉所有msg里的中文字符为对应的日文字符，然后编码的时候直接用shift jis
那其实没有什么要基于tsv的必要了，虽然本来也是charset

https://github.com/hoothin/RadiantHistoriaHans
https://github.com/NinClub/ctr_FontConverter

[Citra]制作bcfnt字体文件
Charset2Bitmap
https://forum.cheatmaker.org/showtopic-3204.aspx

https://github.com/ObsidianX/3dstools

https://geocld.github.io/2020/01/16/rom-hacking/

https://gist.github.com/ngs/2782436

.Net 3DS Toolkit
https://github.com/evandixon/DotNet3dsToolkit

https://github.com/ihaveamac/3DS-rom-tools/wiki/Extract-a-game-or-application-in-.3ds-or-.cci-format

https://github.com/3DSGuy/Project_CTR/blob/master/makerom/README.md

资源黑体
https://github.com/CyanoHao/Resource-Han-Rounded
ResourceHanRoundedCN-Medium

seurapro_13_13 : 
宽18 长21 共246行  
ResourceHanRoundedCN-Medium 字号13px 生成： 宽18 长23

seurapro_12_12 : 
宽17 长20 共246行  
ResourceHanRoundedCN-Medium 字号12px 生成： 宽17 长22

seurapro_12_12.txt第1到10行的编码可能是留给游戏显示特殊符号用的，复制这部分字符以及位图。之后脚本里的信息的符号都换成全角符号

实际上使用的都是seurapro_13_13 整理出来的charset xllt等


流程：
翻译文本 -> build_fake_charset/collect_all_char.py 得到字库，字库xlor等等等
从原本的字体生成图片，放到某处，然后 build_fake_charset/cut_charset_bmp.py 切出来备用
build_fake_charset/build_new_charset_bmp.py 生成新的字库图片，然后用新字库的xlor去生成字库

re_compile_msg/rebuild_msg.py 重新拼接msg文件并且编译并且复制到datacpk文件夹准备打包

手动复制字库文件到cpk文件夹准备打包


回填翻译：
问题：
例如：
[f 0 5 65278][f 2 1][f 4 6 72 2 0 0][f 6 1 2 0 0 7][f 3 1 1 0 0 18]了解だ、[f 6 1 30 0 0 0]。[n][f 1 3 65535][f 1 1][e]
文本会被合并成： 了解だ、。
但因为并不是 [n] 分割，所以控制字符串有三个元素:
['[f 0 5 65278][f 2 1][f 4 6 72 2 0 0][f 6 1 2 0 0 7][f 3 1 1 0 0 18]', '[f 6 1 30 0 0 0]', '[n][f 1 3 65535][f 1 1][e]']
该如何回插呢，之前是完全地切分，但机翻发现会有重复句子（原本是同一行的文本，拆成两次给机翻，机器推断出了句子的意思）。
直接在第一个控制字符后插入吧，都在同一行文本，估计没啥问题。


2024/4/29 10:17:45  Info: (0019:0000) Compiling procedure: e000_140
2024/4/29 10:17:45  Error: (0034:0011) Void-returning function 'function( 8212 ) void WND_FUNCTION_0014(int param1)' used in expression 
2024/4/29 10:17:45  Error: (0034:0011) Failed to emit code for assigment value expression
2024/4/29 10:17:45  Error: (0034:0004) Failed to emit assignment: var0 = (WND_FUNCTION_0014(None 1))
2024/4/29 10:17:45  Error: (0034:0004) Failed to emit variable assignment: var0 = (WND_FUNCTION_0014(None 1))

往回编译的时候会有检查
https://discord.com/channels/746211612981198989/1209607503491498026/1209608672255279114

在F:\modding\persona-tools\Atlus-Script-Tools\Libraries\PersonaQ2\Modules\Window\Functions.json
修改WND_FUNCTION_0014的返回值


2024/4/29 10:43:43  Info: Base directory set to 'D:\code\git\Persona-Modding\classify_sound_file_pq2\cache\event\e800'
2024/4/29 10:43:43  Error: Syntax error: missing ')' at '-32764' (29:26)
2024/4/29 10:43:43  Error: Syntax error: missing ';' at '(' (29:32)
2024/4/29 10:43:43  Error: Syntax error: mismatched input ')' expecting ';' (29:40)
2024/4/29 10:43:43  Error: Syntax error: extraneous input 'else' expecting {'(', ';', '{', '}', '--', '++', '!', '-', 'function', 'global', 'const', 
'ai_local', 'ai_global', 'bit', 'enum', 'local', 'count', 'if', 'for', 'while', 'break', 'continue', 'return', 'goto', 'switch', BoolLiteral, IntLiteral, FloatLiteral, StringLiteral, TypeIdentifier, Identifier} (79:4)
2024/4/29 10:43:43  Info: Parsing compilation unit
2024/4/29 10:43:43  Info: Parsing procedure 'e808_020'

https://discord.com/channels/746211612981198989/746230710150496367/1232988845151092777
就在四天前啊
即使手动去改了 -32764 的负号，也会 报错，单个整数的表达式不合法

那现在只能先这样了，只有前面的bf被替换

正如简介所言，解包工具支持尚不完全，但对于汉化来说并不需要编辑那些没有被工具支持的部分。
有个想法就是直接二进制编辑.bf文件，把汉化并转换后的数据替换并插入到原本日文的位置，并且编辑好文件大小偏移等标志。
https://amicitia.miraheze.org/wiki/BF

另外的话，以前我汉化过一个合p计算器网站，p的名称是存储在TBL文件里的，这是当时用到的脚本（看了下似乎没啥用，能提供下思路也不错）
https://github.com/lraty-li/Persona-Modding/blob/main/zh_hans_for_megaten-fusion-tool/tbl_to_txt.py

这是pq2对应的Wiki
https://amicitia.miraheze.org/wiki/Persona_Q2/Enemies



cri packed file maker 建CPK 的时候必须要压缩，不然黑屏开不了游戏


cpkmakec 命令行显示cpk有 8947个文件
但图形版/ 解包后文件夹 有8948个文件...

靠...cpkmakec输出到打包文件夹了...

ctd就是得自己读取了，文件头16byte，每块文本装在64byte内，很单纯地摆着，用shifjis编码/解码


event/txt/evt_intro...bmd
\event\msg_GAMEOVER.bmd
\event\msg_POEM.bmd

[msg evt_intro_AKECHI]
[f 0 5 65278][f 2 1]岸巌玩癌 悔恢牙永 叶椛快怪[n]永眼鰍苑岩 益翫贋扱雁頑迦屋[n]縞専唄圧遇 詠穫基椛＂眼鰍甘[n]暗扱鴬卯＂ 芽蛾鯵＂裟廠＂ [n][e]

最后一行内有这些文本的时候，会把游戏卡死
去掉 ＂ 试试

＂ 应该没有对应编码，为什么没被替换掉 #BUG


\tutorial\scr  Done
教程

\battle\message Done
战斗中事件文本，技能描述
event Done
Done
\battle\table\playerskillnametable.tbl
\battle\table\enemynametable.tbl
\battle\table\enemyskillnametable.tbl
\battle\table\skillnametable.tbl
\battle\table\personanametable.tbl
f:\TMP\cpk_output_workplace\datacpk\battle\btl_com.bf

\battle\support\message Done
\battle\support\ *.bvp Done
\battle\result Done

Done
\attraction\attrnametable.tbl
\attraction\attrquestnametable.tbl
\attraction\schwalkname.tbl

\camp\cmppoem.bf Done

\camp\dictionary.tbl Done
\camp\skladd_arc Done
\camp\skladdex_arc Done

dungeon\pack\dng_com.arc
\dungeon\pack\field\f01_01.arc
\dungeon\floor_name.tbl 似乎是世界树迷宫的文件
\dungeon\message Done
\dungeon\script\charaTalk Done
Error: Result of void-returning function 'WND_FUNCTION_001E' was used

\dungeon\script\gimmick Done
\dungeon\script\support Done
\dungeon\script\dun_com.bf Done

\facility
arc file?
\facility\pack\cmbroot.arc Done
\facility\pack\shop.arc Done
\facility\pack\top.arc Done
facility/ *.bmd Done
facility/ *.bf Done

init/ *.bmd Done
\init\fcltable.bin Done
\init\itemtbl.bin Done
\init\cmptable.bin Done
\init\qsttable.bin
\init\spkrtbl.bin Done
\init\tutorialtable.bin Done

\interfaceFile\Dungeon.mbm

item/ mbms Done
Done
\Item\seaitemname.tbl
\Item\equipitemnametable.tbl
limititemnametable.tbl
\Item\seaitemequipeffect.tbl
\Item\skyitemequipeffect.tbl
\Item\skyitemname.tbl
\Item\useitemnametable.tbl


\quest\table\questnametable.tbl

\shared\bgm_detail.bmd

\title\nameentry.bin
\title\diff select.bin

mbm 有点头疼
不过这时候才想起来要搜，有老哥在做西班牙语化。但看起来只做了常规的翻译，ctd文件没有翻译
https://github.com/Artur16211/PQ2-Spanish-Mod

f8 01 也许是调用游戏的什么东西，ff才是表示消息结束



ctd:
16 bytes header and end of file
then every 64 bytes is a block of message, 

mbm:
battle\message\skillburstexp.mbm
        0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  
0000h  00 00 00 00 4D 53 47 32 00 00 01 00 84 03 00 00  ....MSG2....„... 
0010h  1E 00 00 00 20 00 00 00 00 00 00 00 00 00 00 00  .... ........... 
0020h  00 00 00 00 0E 00 00 00 00 02 00 00 00 00 00 00  ................ 
0030h  01 00 00 00 0E 00 00 00 0E 02 00 00 00 00 00 00  ................ 
0040h  02 00 00 00 0E 00 00 00 1C 02 00 00 00 00 00 00  ................ 
0050h  03 00 00 00 0E 00 00 00 2A 02 00 00 00 00 00 00  ........*....... 
......
01B0h  19 00 00 00 0A 00 00 00 52 03 00 00 00 00 00 00  ........R....... 
01C0h  1A 00 00 00 0A 00 00 00 5C 03 00 00 00 00 00 00  ........\....... 
01D0h  1B 00 00 00 0A 00 00 00 66 03 00 00 00 00 00 00  ........f....... 
01E0h  1C 00 00 00 0A 00 00 00 70 03 00 00 00 00 00 00  ........p....... 
01F0h  1D 00 00 00 0A 00 00 00 7A 03 00 00 00 00 00 00  ........z....... 
0200h  93 C1 8E EA 83 58 83 4C 83 8B F8 01 FF FF 93 C1  “ÁŽêƒXƒLƒ‹ø.ÿÿ“Á 
0210h  8E EA 83 58 83 4C 83 8B F8 01 FF FF 93 C1 8E EA  ŽêƒXƒLƒ‹ø.ÿÿ“ÁŽê 
0220h  83 58 83 4C 83 8B F8 01 FF FF 8D 55 8C 82 83 58  ƒXƒLƒ‹ø.ÿÿ

0000h - 001Fh :
file header: size: 32 bytes
    000c - 000f: whold file size: 00 00 03 84
    0010 - 0013: message count(00 00 00 1E of this skillburstexp.mbm, 00 ~ 1D)
    other seems to be same for every file
0020h - 01F0h :
every message's infomation, size: 16 bytes
    0020h-002Fh: the first message's infomation(index 0), 
        0020h - 0023h: 00 00 00 00H, index 0
        0024-0027:
        0025h: high byte of length of message 00
        0024h: low byte of length of message 0e
        so the length of message 0 is 00 0eh, 14 bytes
        
        0028-002b:
        0029h: high byte of start location(offset) of message 02
        0028h: low byte of start location of message 00
        so the start offset of message is 02 00h,
        the message start from 0200h to 0200h + 000eh = 02 0eh: 93 C1 8E EA 83 58 83 4C 83 8B F8 01 FF FF

0200h - EOF: messages are stored here

if high byte is F8, it seens to be some kind of function invoking, should by pass itself and some bytes fllowing it(if needed).
since f8 xx could not be decode by shift-jis  

    

e800 无法反编译：
把msg编译为bmd，然后接到bf的message部分即可，内容是差不多的，注意bf文件头的文件大小
note_image/2024-05-22 08 30 07

bf文件的05cH是msg部分的起始位置偏移 两byte，低位在前
0004h-0005h 跟 0006c 0006d 总是相同？是message的结束位置

fcltable.bin:
文件块有些不是64 bytes 了

ftd:
\init\fcltable_bin_cache\fclHelpTable_SHOP.ftd
50 01 00 00 06 00 00 00
0150 / 00 06 = 38 ，每行文本的宽度?

策略：读掉16bytes 文件头，然后按行宽读取每条信息。
并且例如 00 00 15 00 00 这种不知道干嘛的分隔符一样的东西，保留原样。
msg的话在分块完之后，再每块按 00 00 切开，这样比较好避开分隔符解析的问题(以及 ff ff)

反复按行宽大小读取，如果剩下的byte数量小于行宽，一般应该是刚好是header大小，不是的话报错看看啥情况


https://discord.com/channels/746211612981198989/1046037499056762911/1179184941691588699
PUT prints only numbers
PUTS prints only text
PUTF prints only floats

battle/event/support/msg 的flow里面有很多文本，看来只是print

fail to rebuild, like event 800
['noffice.bf.flow.bf', 'scrgotodungeon.bf.flow.bf', 'townsupport.bf.flow.bf', 'weapon.bf.flow.bf']

ori-data\event\e100\e100_155.bf
打包后的 event\e100\e100_155.bf
对比函数部分：(	Instruction data)
原本是： 09 00 00 00 09 00 00 00 函数部分 09 00 00 00 
打包后： 09 00 00 00 函数部分 09 00 00 00 
也许是优化掉了？不管估计没事

符号部分：
总56字节，最后一个字节是某种偏移，打包后的总是比打包前的小1，跟 Instruction data 部分少4字节有关？

对比比较大的e100_172
符号部分很多 ifelse_label_*， 文件的 0030，004Fh 有所变化，那能不能完全不动呢？

要动的部分：文件整体大小、message 部分大小（可以在bmd的文件头找到）

\init\itemtbl.bin
既然文本的数据都是22字节一块的，也许没有记录长度的地方，试试直接换成中文


facility/pack/shop 
打包失败？
amicitia打包会去添加一些空字符，偏移也被修改

arc:
文件头：4 字节
子文件名：20h（32） 字节 
下一块的文件大小：2字节
内容
子文件名：20h（32） 字节 
下一块的文件大小：2字节
内容
。。。
？

ori 
4 + 20h+ 55c9 +4 = 55f1
55f1 + 20h +4 + 5e5c  = b471?
b471 + 20h +4 + 22e8c = 2e321
2e321 + 20h +4 + 4105b8 = 43e8fd (刚好是文件尾)

repacked with amicitia (pakpack has different file order, hard to compare)
4 + 20 + 4+ 55e0 = 5608
5608 + 20h +4 + 5e60 = b48c
b48c + 20h +4 + 22ea0 = 2e350
b48c + 20h +4 + 4105c0 = 43e910 (还有空余字符)

手动把中间的 00 去掉跟修下偏移之后，就正常了，即使最后不指向文件尾也没关系
#TODO issue

话说看了下西班牙语上的shop.arc，也是有00 填充的，怎么他的没事...

charset fixing
①


F:\TMP\cpk_output_workplace\ori-data\attraction\schwalkname.tbl
F:\TMP\cpk_output_workplace\ori-data\battle\ai\scr_bos_elizabeth_z.bf

TODO rebuild all 少了待机时右上角信息

进天鹅绒会崩溃，替换
cmbroot.arc
后正常
修复arc文件头


bvp

01 00 03 00 D0 08 00 00 7B 01 00 00
01 00 01 00 50 0A 00 00 A6 00 00 00

D0 08: msg start location
7b 01: msg file size


format of 『』lost, should enable inline index for some file
enabled format keeping:
zh/camp/skladd_arc
zh/camp/skladdex_arc
zh/battle/message
zh/battle/result/ bmd 
zh/battle/result/persona_get_bin bmd 

zh/facility/bmd.py
msg_usercmm
msg_trade
msg_book
msg_costume
msg_market
msg_sklcard
不知为何都被控制字符分割为单字
目前需要分割的只有 msg_combine,msg_weapon

zh/facility/cmbroot/
msg_combine_lvup
msg_combine

event


event关闭合并为一行，不然比如其他游戏主角的文本会因为换行符插入而混乱

BUG:
出现很多X，因为00填充吗？
额外的换行：翻译后文本比较长，被额外插入换行符。但如果关闭了合并为一样，原本的换行符也起作用

战斗时效果提示

