from PIL import Image
import pytesseract
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image to be OCR'd")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])

text = pytesseract.image_to_string(Image.open(args["image"]), config= "-l chi_sim --psm 10")

print(text)
cv2.imshow("img",image)
cv2.waitKey(0)
