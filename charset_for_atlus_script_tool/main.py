# -*- coding: UTF-8 -*-
import os
import time
from annoy import AnnoyIndex
from build_annoy_index import buildAnnoyIndex
from build_tsv import buildTsv
from calc_surrogates import genCharSurrogates
from common import dumpJson, loadJson
from cut_Image import cutImage
from gen_all_font_preview import gen_font_all_image, get_char_list_from_ttf
from search_annoy import loadAnnoyIndex, searchAnnoy

class Timer:
    sTime = ''
    def __init__(self, time):
        Timer.sTime = time
    def timeStop(self, msg):
        print("{} with {}s".format(msg, int(time.time() - Timer.sTime)))
        Timer.sTime = time.time()
    def reset(self):
        Timer.sTime = time.time()

# cut image 

timer = Timer(time.time())
FONT0 = 'FONT0.PNG'
croppedOutputFolder = "cropped"
GLYPH_SIZE = 96
VECTOR_DIM = 4096
N_TREES = 50
THREADHOLD = 0.89
SEARCH_K = 30000

### cut FONT0.PNG
cutImage(FONT0, croppedOutputFolder)

for folder in ['cache','tsv','surrogates']:
  if(not os.path.exists(folder)):
    os.mkdir(folder)

timer.timeStop("done cutting {}".format(FONT0))

fonts = os.listdir('font')
# DEBUG BEGIN 
# fonts = ["dfyuanlightbold.ttf"]
# DEBUG END

for font in fonts:

    timer.reset()
    fontName = font[:-4]
    fontImagesPath  = "font_img_{}".format(fontName)
    ### gen preview image of font
    gen_font_all_image(os.path.join("font", font), fontImagesPath)
    timer.timeStop("generated previws for {} ".format(fontName))

    annoyPath = os.path.join('cache','ttf_annoy_{}.ann'.format(fontName))
    ### build annoy index ###
    ann = AnnoyIndex(VECTOR_DIM, "dot")
    buildAnnoyIndex(ann, fontImagesPath,annoyPath , n_trees = N_TREES)
    timer.timeStop("builded annoy index for {} ".format(fontName))

    ann = None
    ann2 = AnnoyIndex(VECTOR_DIM, "dot")
    # cause some time need to remakr the buildAnnoyIndex, adjust THREADHOLD
    annoy = loadAnnoyIndex(ann2, annoyPath)
    ### search with game's char image 
    searchAnnoy(annoy, croppedOutputFolder, fontName, similarityThreadHold=THREADHOLD, search_k=SEARCH_K)
    timer.timeStop("searched annoy for {} ".format(fontName))

    ### build tsv
    # TODO calc by grapth size
    charSum = 16 * 471 # how many characters in FONT0.png
    # TODO  clear shits like: "gameChar_Numbering2Char"
    comparisonTable = loadJson(os.path.join('cache',"gameChar_Numbering2Char_{}.json".format(fontName)))

    # 偏0x20 是FONT0.fnt 没有, 看看现有charset 的 csv:
    # \u0000	\u0001	~	\u001e	\u001f
    buildTsv(charSum, comparisonTable, os.path.join("tsv","tsv_{}.tsv".format(fontName)))
    ### generate [char : surrogates] txt
    genCharSurrogates(comparisonTable, os.path.join('surrogates', "surrogates_{}.txt".format(fontName)))
