import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Activation
from keras.layers.core import Flatten, Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
from keras.preprocessing.image import ImageDataGenerator
from keras import applications
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import optimizers
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

datagen = ImageDataGenerator(rescale=1./255)

train_path = 'cell_images/'

train_batches = ImageDataGenerator().flow_from_directory(train_path, target_size=(115,115),
                                                         classes=['Parasitized','Uninfected'], class_mode='categorical',
                                                         batch_size=27560)

imgs, label = next(train_batches)
print(label.shape)
print(imgs.shape)

X_train, X_test, y_train, y_test = train_test_split(imgs,label,test_size=0.3,random_state=42)

datagen = ImageDataGenerator(
        rotation_range=10,  # Rotate images randomly
        zoom_range = 0.1, # Zoom images randomly
        width_shift_range=0.1,  # Horizontally shift images in random order
        height_shift_range=0.1  # Vertically shift images in random order
)

datagen.fit(X_train)

for i in range (0,5):
    image = imgs[i]
    plt.imshow((image * 255).astype(np.uint8))
    if (label[i][0]==1):
      print("Parasitized")
    if (label[i][1]==1):
        print("Uninfected")
    plt.show()


# Confusion Matrix
def show_confusion_matrix(history, model, x_test, y_test):
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    pre_cls = model.predict_classes(x_test)

    # Decode from one hot encoded to original for confusion matrix
    decoded_label = np.zeros(x_test.shape[0], )
    for i in range(y_test.shape[0]):
        decoded_label[i] = np.argmax(y_test[i])
    # print(decoded_label.shape)

    cm1 = confusion_matrix(decoded_label, pre_cls)
    print('Confusion Matrix : \n')
    print(cm1)


# model1 freeze all layers
# VGG16 pre-trained model
image_w, image_h = 115, 115
model1 = applications.VGG16(weights="imagenet", include_top=False, input_shape=(image_w, image_h, 3))
model1.summary()

# Freezing all the layers
for layer in model1.layers[:]:
    layer.trainable = False

# Trainable layers
print("Trainable Layers:")
for i, layer in enumerate(model1.layers):
    print(i, layer.name, layer.trainable)

# Adding custom layers to create a new model
new_model = Sequential([
    model1,
    Flatten(name='flatten'),
    Dense(256, activation='relu', name='new_fc1'),
    Dropout(0.5),
    Dense(2, activation='softmax', name='new_predictions')
])
new_model.summary()


new_model.compile(loss = "categorical_crossentropy", optimizer = optimizers.Adam(lr=0.0001), metrics=["accuracy"])

#Fitting the model on the train data and labels.
print("Batch Size: 10, Epoch: 5, Optimizer: Adam")
new_model.fit(imgs, label, batch_size=10, epochs=2, verbose=1, validation_split=0.30, shuffle=True)

new_model.save('malaria.h5')




