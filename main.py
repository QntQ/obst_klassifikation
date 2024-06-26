import cv2
import numpy as np
import os
import tensorflow as tf


def confusion_matrix(predictions, labels):

    matrix = np.zeros((2, 2))

    for i in range(len(predictions)):

        if predictions[i] > 0.5:
            prediction = 1
        else:
            prediction = 0

        matrix[prediction][labels[i]] += 1

    return matrix


def load_data(pathes):

    images = []
    labels = []
    apple_path, banana_path = pathes

    for i in os.listdir(apple_path)[:750]:
        img = cv2.imread(apple_path + i)
        img = cv2.resize(img, (360, 360))/255

        images.append(img)
        labels.append(0)

    for i in os.listdir(banana_path)[:750]:
        img = cv2.imread(banana_path + i)
        img = cv2.resize(img, (360, 360))/255

        images.append(img)
        labels.append(1)

    images = np.array(images)
    labels = np.array(labels)

    return images, labels


def create_tensorflow_model():

    # initializing Sequential model
    model = tf.keras.models.Sequential()

    # adding layers to the model
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                                     input_shape=(360, 360, 3)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))

    # flattening the model
    model.add(tf.keras.layers.Flatten())

    # adding dense layers
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # compiling the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


def main():

    # pathes for training data
    apple_path = 'data_training/Apple/'
    banana_path = 'data_training/Banana/'

    images, labels = load_data([apple_path, banana_path])

    if not os.path.exists('model.h5'):

        model = create_tensorflow_model()

        # training the model for 10 epochs, increase number if epochs for longer training
        model.fit(images, labels, epochs=10)

        model.save('model.h5')

    else:

        model = tf.keras.models.load_model('model.h5')
    # pathes for testing data, should be different from training data for better evaluation

    apple_path = 'data_testing/Apple/'
    banana_path = 'data_testing/Banana/'

    images, labels = load_data([apple_path, banana_path])

    predictions = model.predict(images)

    matrix = confusion_matrix(predictions, labels)

    print(matrix)

    accuracy = (matrix[0][0] + matrix[1][1]) / np.sum(matrix)

    print("Accuracy: ", accuracy)


if __name__ == '__main__':
    main()
