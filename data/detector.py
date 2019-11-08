import numpy as np
from PIL import Image
from selective_search import selective_search
from classifier import predict, predict_init

predict_init()
image_shape = (32, 32)
CONFIDENCE_THRESHOLD = 0.8  # minimum probability of predicted label


def detect_objects(image):
    """Determine the label and location of objects in an image.

    Returns a list of tuples (label, x, y, w, h) corresponding to all object
    labels and locations with probability above the confidence threshold.
    """
    candidates = list(selective_search(image))
    sub_images = np.array([*map(lambda i: np.array(Image.fromarray(image[i[1]:i[1] + i[3], i[0]:i[0] + i[2], :]).resize(image_shape), dtype=np.uint8)/255, candidates)])
    predict_probabilities = predict(sub_images)
    predict_labels = np.argmax(predict_probabilities, axis=1)
    return [(predict_labels[i], *candidates[i]) for i in range(len(candidates)) if predict_probabilities[i][predict_labels[i]] > CONFIDENCE_THRESHOLD]
    
    
if __name__ == "__main__":
    objects = detect_objects(np.array(Image.open("test.png"))[:, :, :3])
    print(objects)
