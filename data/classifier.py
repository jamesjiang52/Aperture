import h5py
import tflearn.data_preprocessing
import tflearn.data_augmentation
from tflearn.layers import core, conv, estimator
from tflearn.models import dnn


h5f = h5py.File("dataset.h5", "r")
X = h5f["X"]
Y = h5f["Y"]

data_preprocessing = tflearn.data_preprocessing.DataPreprocessing()
data_preprocessing.add_featurewise_stdnorm()
data_preprocessing.add_featurewise_zero_center()

data_augmentation = tflearn.data_augmentation.ImageAugmentation()
data_augmentation.add_random_flip_leftright()
data_augmentation.add_random_flip_updown()
data_augmentation.add_random_rotation(max_angle=180)

# shape is 480x480x3
network = core.input_data(shape=(None, 480, 480, 3), data_preprocessing=data_preprocessing, data_augmentation=data_augmentation)
network = conv.conv_2d(network, nb_filter=6, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=6, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=4, strides=4, padding="same")

# shape is 120x120x6
network = conv.conv_2d(network, nb_filter=12, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=12, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

# shape is 60x60x12
network = conv.conv_2d(network, nb_filter=24, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=24, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

# shape is 30x30x24
network = conv.conv_2d(network, nb_filter=48, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=48, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

# shape is 15x15x48
network = conv.conv_2d(network, nb_filter=96, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=96, filter_size=5, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=3, strides=3, padding="same")

# shape is 5x5x96
network = core.fully_connected(network, n_units=256, activation="relu", regularizer="L2")
network = core.fully_connected(network, n_units=256, activation="relu", regularizer="L2")
network = core.fully_connected(network, n_units=6, activation="linear", regularizer="L2")
network = estimator.regression(network, optimizer="adam", loss="softmax_categorical_crossentropy")

model = dnn.DNN(network)
model.fit(X, Y, validation_set=0.2, show_metric=True)
