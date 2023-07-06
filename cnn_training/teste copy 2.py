import tensorflow as tf
import keras
import os
from keras import datasets, layers, models
from keras.preprocessing.image import ImageDataGenerator




train = ImageDataGenerator(rescale=1/255)
train_dataset = train.flow_from_directory('/home/luis/tcc/tcc/DEV/TKinterExample-master/dataset/', target_size = (245,640), batch_size = 5, class_mode = 'categorical', color_mode="rgb")
test_dataset = train.flow_from_directory('/home/luis/tcc/tcc/DEV/TKinterExample-master/dataset_test/', target_size = (245,640), batch_size = 1, class_mode = 'categorical', color_mode="rgb")
 

CLASSES = 10
# setup model

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(245, 640, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(CLASSES, activation='softmax'))

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


#checkpoint_path = "training_1/cp.ckpt"
#checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
#cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                 save_weights_only=True,
#                                                 verbose=2)

#history = model.fit(train_dataset, epochs=20, verbose=2,callbacks=[cp_callback])


#model.load_weights(checkpoint_path)
MODEL_FILE = 'Custom.model'
model.fit(train_dataset, epochs=40, verbose=2)
model.save(MODEL_FILE)

test_loss, test_acc = model.evaluate(test_dataset, verbose=2)
print(f'loss:{test_loss} acc: {test_acc}')