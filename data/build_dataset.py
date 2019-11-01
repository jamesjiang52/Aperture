import os
from PIL import Image
from tflearn.data_utils import build_hdf5_image_dataset

image_shape = (32, 32)
dataset_file = "classes.txt"
output_path = "dataset.h5"

for file_name in os.listdir("."):
    if os.path.isdir(file_name):
        for image_name in os.listdir(file_name):
            image_path = "{}/{}".format(file_name, image_name)
            image = Image.open(image_path)
            image = image.resize(image_shape)
            image.save(image_path)

build_hdf5_image_dataset(
    dataset_file,
    image_shape=image_shape,
    output_path=output_path,
    mode="file",
    categorical_labels=True,
    normalize=True,
    grayscale=False
)
