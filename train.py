import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import optimizers
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	print('training.py initialized')

	img_size = 256
	data = np.load('processed_images.npy')
	labels = np.load('processed_labels.npy')

	print("Data shape", data.shape)
	print("Labels shape", labels.shape)

	X_train, X_test, y_train, y_test = train_test_split(data, labels, train_size = 0.8, random_state = 20)

	nb_classes = 2
	y_train = np.array(y_train)
	y_test = np.array(y_test)
	Y_train = to_categorical(y_train, nb_classes)
	Y_test = to_categorical(y_test, nb_classes)

	X_train = X_train.astype('float32')
	X_test = X_test.astype('float32')

	print("Training matrix shape", X_train.shape)
	print("Testing matrix shape", X_test.shape)

	print("Training label shape", Y_train.shape)
	print("Testing label shape", Y_test.shape)

	model = VGG19(weights = "imagenet", include_top=False, input_shape = (img_size, img_size, 3))
	#model.summary()

	top_model = Sequential()
	top_model.add(Flatten(input_shape=model.output_shape[1:]))
	top_model.add(Dense(128, activation='relu'))
	top_model.add(Dropout(0.5))
	top_model.add(Dense(2, activation='softmax'))

	new_model = Sequential()
	for layer in model.layers: 
	    new_model.add(layer)
	    
	new_model.add(top_model)

	for layer in model.layers[:21]:
		layer.trainable = False

	adam = optimizers.SGD(lr=1e-4, decay=1e-6, momentum=0.9, nesterov=True)
	new_model.compile(loss='categorical_crossentropy', optimizer= adam, metrics=['accuracy'])

	new_model.fit(X_train, Y_train, batch_size=64, nb_epoch=10, verbose=2 )

	score = new_model.evaluate(X_test, Y_test, verbose=0)
	print("Loss: " + str(score[0]))
	print("Accuracy: " + str(score[1]))

	new_model.save('model.h5')