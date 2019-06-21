#import statements
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

#Predict Function
def xpredict(model_path, image_path):
    #Importing model
    model = load_model(model_path)
    #Shape of the model
    image_shape = (152,)
    #Loading Image
    import cv2
    img = cv2.imread(image_path)
    img = cv2.resize(img, image_shape[0:2])
    img = img/255.0
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    return preds


