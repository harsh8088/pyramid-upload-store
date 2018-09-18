import glob
import os

from PIL import Image


def resize_pil_image():
    size = 256, 256
    for infile in glob.glob("/home/harsh/Dev/Samples/pyramid-upload-store/upload_images/*"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        im.thumbnail(size)
        im.save(file + "_thumbnail", "JPEG")


def scale_pil_image():
    for infile in glob.glob("/home/harsh/Dev/Samples/pyramid-upload-store/upload_images/*"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        w, h = im.size
        new_size = [w + 200, h + 200]
        im.thumbnail(new_size)
        im.save(file + "_thumbnail.png", "JPEG")


if __name__ == '__main__':
   resize_pil_image()
