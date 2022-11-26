# -*- coding: UTF-8 -*-
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import os
import shutil  

from common import dumpJson

#https://www.likefont.com/font/2295308/#download


def get_char_list_from_ttf(font_file):
    ' 给定font_file,获取它的中文字符 '
    f_obj = TTFont(font_file)
    m_dict = f_obj.getBestCmap()
    
    unicode_list = []
    for key, _ in m_dict.items():
        unicode_list.append(key)
        
    char_list = []
    for ch_unicode in unicode_list:
        #https://unicode-table.com/cn/blocks/private-use-area/
        # filter out \uE000—\uF8FF
        # charUniCode = hex(ch_unicode)
        if(0xE000 <= ch_unicode and ch_unicode <= 0xF8FF):
            continue
        char_list.append(chr(ch_unicode))

    # filter out control charater for dfyuanlightbold
    # char_list = char_list[32:126] + char_list[127:-1]
  
    return char_list
 
def draw_png(char, outputPath,font, image_size = 96):
    # text_width, text_height = font.getsize(char)
    image = Image.new(mode='L', size=(image_size, image_size))
    draw_table = ImageDraw.Draw(im=image)
    # guess
    leftTop = 15
    draw_table.text(xy=(leftTop, leftTop), text=char, fill='#FFFFFFFF', font=font)
    
    image.save(outputPath, 'PNG')
    # print("done {}".format(char))
    image.close()

def gen_font_all_image(fontPath, imgOutputPath):

    fontName = fontPath.split(os.sep)[-1][:-4]
    
    chars = get_char_list_from_ttf(fontPath)

    numberingToChar = dict(enumerate(chars))
    charToNumbering = dict(zip(numberingToChar.values(),numberingToChar.keys()))
    dumpJson(numberingToChar,os.path.join('cache',"ttf_comparison_table_numberingToChar_{}.json".format(fontName)))
    dumpJson(charToNumbering,os.path.join('cache',"ttf_comparison_table_charToNumbering_{}.json".format(fontName)))

    if(os.path.exists(imgOutputPath)):
      shutil.rmtree(imgOutputPath)  
    os.mkdir(imgOutputPath)  
  
    font_size = 66
    font=ImageFont.truetype(fontPath, font_size)
    for char in chars:
        try:
            imgPath = os.path.join(imgOutputPath, "{}.png".format(charToNumbering[char]))
            draw_png(char, imgPath, font)
        except Exception as e:
            print(char, ' ERR: ', e)
            continue

if __name__ == "__main__":
    font = "./font/dfyuanlightbold.ttf"
    fontName = font[:-4]
    fontImagesPath  = "font_img_{}".format(fontName)
    gen_font_all_image(os.path.join("font",font), "font_img_{}".format(fontName))

