# -*- coding: UTF-8 -*-
import os
from annoy import AnnoyIndex
from common import dumpJson, loadJson
from cos_compare import img2Vetor
from PIL import Image



# filePath = '../cropped/5300.png'

def loadAnnoyIndex(annoy, annoyIndexPath, warmUp = False):
  annoy.load(annoyIndexPath, prefault= True) # super fast, will just mmap the file
  if (warmUp):
    # https://github.com/spotify/annoy/issues/376
    # MAP_POPULATE not defined on windows 
    sum = annoy.get_n_items()
    for i in range(sum):
      annoy.get_item_vector(i)
  return annoy

    
def filterMaxNumbering(result):
  # result[0] indexing
  # result[1] similarity
  zipped = list(zip(result[0], result[1]))
  qualified = list(filter(lambda x: x[1] > SIMILARITY_THREAD, zipped))
  qualifiedKeys = [k[0] for k in qualified]
  if(len(qualifiedKeys) >= 1):
  # get the max indexing?
    return qualified[qualifiedKeys.index(max(qualifiedKeys))][0]
  return -1
  
def searchAnnoy(annoy, targetImgPath,fontName, similarityThreadHold, search_k):
  ttf_numbering2Char = loadJson(os.path.join('cache',"ttf_comparison_table_numberingToChar_{}.json".format(fontName)))
  targetImgs = os.listdir(targetImgPath)
  gameCharNumbering2Char = {}
  for fileName in targetImgs:
    image = Image.open(os.path.join(targetImgPath, fileName))
    # DEBUG BEGIN
    # image = Image.open(os.path.join(target_image_folder, '6330.png'))
    # DEBUG END
    try:
      vetcor = img2Vetor(image)
    except Exception :
      # norm is zero
      continue
    # DEBUG BEGIN
    # b = annoy.get_item_vector(20886)
    # res = np.dot(vetcor, b)
    # DEBUG END
    result = annoy.get_nns_by_vector(vetcor, 1 , search_k = search_k ,include_distances=True)

    # get the max indexing to void  火 -> (火)， 字体问题
    # resultIndex = filterMaxNumbering(result)
    
    resultIndex = result[0][0] if result[1][0] > similarityThreadHold else -1 
    # print(result)
    if (resultIndex > 0):
      gameCharNumbering2Char[fileName] = ttf_numbering2Char[str(resultIndex)]

  # TODO gameCharNumbering2Char 不应该有重复值
  dumpJson(gameCharNumbering2Char, os.path.join('cache','gameChar_Numbering2Char_{}.json'.format(fontName)))

  
if __name__ == "__main__":
  target_image_folder = os.path.join("cropped")
  VECTOR_DIM = 4096
  SIMILARITY_THREAD = 0.93

  ann = AnnoyIndex(VECTOR_DIM, 'dot')
  font = "dfyuanlightbold.ttf"
  fontName = font[:-4]
  font_all_image = "font_img_{}".format(fontName)
  annoy = loadAnnoyIndex(ann, 'ttf_annoy_{}.ann'.format(fontName))
  searchAnnoy(annoy, target_image_folder, fontName, SIMILARITY_THREAD, 30000)
