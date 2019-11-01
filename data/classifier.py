import h5py
import tflearn.data_preprocessing
import tflearn.data_augmentation
from tflearn.layers import core, conv, estimator
from tflearn.models import dnn


dataset_filepath = "dataset.h5"
model_filepath = "classifier.tfl"

data_preprocessing = tflearn.data_preprocessing.DataPreprocessing()
data_preprocessing.add_featurewise_stdnorm()
data_preprocessing.add_featurewise_zero_center()

data_augmentation = tflearn.data_augmentation.ImageAugmentation()
data_augmentation.add_random_flip_leftright()
data_augmentation.add_random_flip_updown()
data_augmentation.add_random_rotation(max_angle=180)

network = core.input_data(shape=(None, 32, 32, 3), data_preprocessing=data_preprocessing, data_augmentation=data_augmentation)
network = conv.conv_2d(network, nb_filter=32, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=32, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

network = conv.conv_2d(network, nb_filter=64, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=64, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

network = conv.conv_2d(network, nb_filter=128, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=128, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

network = conv.conv_2d(network, nb_filter=256, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=256, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

network = conv.conv_2d(network, nb_filter=512, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.conv_2d(network, nb_filter=512, filter_size=3, strides=1, padding="same", activation="relu", regularizer="L2")
network = conv.max_pool_2d(network, kernel_size=2, strides=2, padding="same")

network = core.fully_connected(network, n_units=1024, activation="relu", regularizer="L2")
network = core.fully_connected(network, n_units=1024, activation="relu", regularizer="L2")
network = core.fully_connected(network, n_units=6, activation="linear", regularizer="L2")
network = estimator.regression(network, optimizer="adam", loss="softmax_categorical_crossentropy", learning_rate=0.001)

model = dnn.DNN(network)


def train_model():
    h5f = h5py.File(dataset_filepath, "r")
    X = h5f["X"]
    Y = h5f["Y"]

    model.fit(X, Y, n_epoch=200, validation_set=0.2, show_metric=True)
    model.save(model_filepath)
    
    
def predict_label(X):
    model.load(model_filepath)
    model.predict_label(X)
