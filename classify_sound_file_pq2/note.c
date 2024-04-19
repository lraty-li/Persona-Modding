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