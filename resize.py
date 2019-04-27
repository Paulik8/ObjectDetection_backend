from PIL import Image
import os
from tornado import gen

# path = "/home/paul/PycharmProjects/models/cat-and-dog.jpg"
image_path = "/home/paul/PycharmProjects/diplom/backend/images"
saving_file = "/home/paul/PycharmProjects/diplom/backend/images_s"


@gen.coroutine
def resize(file):
    file_name = file
    image_file = os.path.join(image_path, file_name)
    # for file in os.listdir(path):
    #     image_file = os.path.join(path, file)
    img_org = Image.open(image_file)
    # get the size of the original image
    width_org, height_org = img_org.size
    # set the resizing factor so the aspect ratio can be retained
    # factor > 1.0 increases size
    # factor < 1.0 decreases size
    factor = 0.25
    width = int(width_org * factor)
    height = int(height_org * factor)
    # best down-sizing filter
    img_anti = img_org.resize((width, height), Image.ANTIALIAS)
    # split image filename into name and extension
    name, ext = os.path.splitext(file_name)
    # create a new file name for saving the result
    new_image_file = "%s%s%s" % (name, str(factor), ext)
    # img_anti.save("./images0.5/" + file)
    img_anti.save(os.path.join(saving_file, name), img_org.format)
