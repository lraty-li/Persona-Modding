# 为 atlus script tools 添加简中字符集

## 提醒

如果你在寻找 字-字库编码 的对照，这是一份手工维护的字库编码表，强烈建议优先使用: [bilibili 专栏](https://www.bilibili.com/read/cv19937910)

## 主要流程

- 利用[Persona editor](https://github.com/Meloman19/PersonaEditor), 从FONT0.FNT中提取出FONT0.PNG
- 将FONT0.PNG 截割成每个字符单独的图片(96*96)
- 寻找看起来像FONT0.PNG使用到的字体
- 生成字体文件的所有文字的图片，并且手动调整到跟从FONT0.PNG切割出来的那些图片相近（字的位置，字体大小）。
- 计算字体文件图片的向量，存入[annoy](https://github.com/spotify/annoy)文件。会跳过没有可视字符（纯黑）的图片
- 计算FONT0.PNG的图片的向量，搜索与其最相似的字体图片。这里使用的是余弦相似度。

## 使用

将FONT0.PNG放到main.py的同级位置，新建font文件夹，把所有看起来跟FONT0.PNG相近的字体放到font文件夹中。运行main.py。

main.py中的THREADHOLD控制相似度，不要调太高。N_TREES与SEARCH_K则是见[annoy api]([SEARCH_K](https://github.com/spotify/annoy#full-python-api)), 这里写得比较高，不过不是很在乎时间。

输出结果将会出现在 tsv, surrogates 文件夹中，没识别到的会用 * 号填充。将tsv文件放到Atlus-Script-Tools 的 Charsets 文件夹下，之后使用的时候:

```bash
-Encoding 文件名
```

## 其他

- 这里使用的是 p5r xgp 的简中的FONT0。
- 并不会因为是不是生僻字而区别识别成功与否，所以建议使用开头提及的版本。
- tsv_compare.py 会读取tsv文件夹下所有tsv，然后检查对应字符是不是一致，然后输出一个excel文件。
- 在尝试利用Persona editor导出繁中的FONT0.fnt的时候，会因为图片尺寸过大而无法导出(1535*83040), 通过缩小图片尺寸导出发现后半截有很多重复，不清楚原因。

  ```c#
  //DEBUG BEGIN
  //https://github.com/Meloman19/PersonaEditor/blob/master/AuxiliaryLibraries.WPF/Tools/ImageTools.cs#L21
  var scaleFactor = 0.75d;
  var resizedBitmap = new TransformedBitmap(image, new ScaleTransform(scaleFactor, scaleFactor));
  //DEBUG END
  encoder.Frames.Add(BitmapFrame.Create(resizedBitmap));
  //encoder.Frames.Add(BitmapFrame.Create(image));
  ```

- 字体文件并不一定一一对应，例如 "㈫"(\u322b), 在"华康细软bold" 对应到了"火", 会导致识别出来的tsv中"火"字对应到了"㈫"
- get_char_list_from_ttf 中为 "华康圆体简繁"字体 过滤掉了私用区的字符.
- 总的来看华康圆体简繁-Std-W9的准确率比较高.
