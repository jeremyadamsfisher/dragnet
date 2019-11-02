import PIL
from app import translate
from pathlib import Path

test_img_fp = Path.cwd()/"test_data"/"profile.jpeg"
assert test_img_fp.exists()

def test():
    img = PIL.Image.open(test_img_fp)
    translate.translate(img)
    img.save("./test.jpg")

test()
