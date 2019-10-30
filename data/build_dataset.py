from tflearn.data_utils import build_hdf5_image_dataset

dataset_file = "classes.txt"
image_shape = (480, 480)
output_path = "dataset.h5"

build_hdf5_image_dataset(
    dataset_file,
    image_shape=image_shape,
    output_path=output_path,
    mode="file",
    categorical_labels=True,
    normalize=True,
    grayscale=False
)
