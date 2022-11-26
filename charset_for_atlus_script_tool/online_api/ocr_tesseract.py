import pytesseract
import os
from PIL import Image

imaegFolderBase = "cropped-preProgressed"

config_chi_sc = "-l chi_sim --psm 10"
chi_sc = (749,7529)

def imageToString(starting, ending, config):
  for numbering in range(starting, ending+1):
    text = pytesseract.image_to_string(Image.open(os.path.join(imaegFolderBase, "{}.png".format(numbering))), config= config)
    print(text)

# 识别中文
imageToString(chi_sc[0], chi_sc[-1], config_chi_sc)
