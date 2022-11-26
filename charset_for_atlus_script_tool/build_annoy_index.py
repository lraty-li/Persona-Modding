# -*- coding: UTF-8 -*-
from cos_compare import img2Vetor
from PIL import Image
import os

from annoy import AnnoyIndex

def buildAnnoyIndex(annoy, fontImagePath, annoyPath, n_trees):
  images = os.listdir(fontImagePath)
  for img in images:
    imgName = img[:-4] #".png"

    # Elasticsearch？
    image = Image.open(os.path.join(fontImagePath, img))
    try:
      vetcor = img2Vetor(image)
      annoy.add_item(int(imgName), vetcor)
    except Exception :
      # norm is zero
      continue
  # build annoy index
  annoy.build(n_trees)
  annoy.save(annoyPath)
  return annoy



# https://github.com/currentslab/awesome-vector-search


if __name__ == "__main__":
  # 4096 = 64*64 , get_thum
  VECTOR_DIM = 4096
  ann = AnnoyIndex(VECTOR_DIM, "dot")

  font = "dfyuanlightbold.ttf"  
  fontName = font[:-4]
  font_all_image = "font_img_{}".format(fontName)
  buildAnnoyIndex(ann,font_all_image,'ttf_annoy_{}.ann'.format(fontName), n_trees = 50)

  # images = os.listdir(font_all_image)
  # charToVetctor = {}
  # for img in images:
  #   imgName = img[0:-4] #".png"

  #   # Elasticsearch？
  #   image = Image.open(os.path.join(font_all_image, img))
  #   vetcor = img2Vetor(image)
  #   ann.add_item(int(imgName), vetcor)

  # # build annoy index
  # ann.build(40)
  # ann.save('ttf_annoy.ann')
  # np.save("ttf_charToVetor.npy",charToVetctor ,allow_pickle=True)

    
