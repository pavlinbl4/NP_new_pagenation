from openpyxl.drawing.image import Image


def image_resize(image_path):
    img = Image(image_path)
    img.width //= 3
    img.height //= 3
    return img
