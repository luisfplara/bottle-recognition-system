from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import time
CLASSES = 7
# setup model
base_model = InceptionV3(input_shape=(245, 640,3),weights='imagenet', include_top=False)
base_model.summary()


new_model = base_model.output

new_model = GlobalAveragePooling2D(name='avg_pool')(new_model)
new_model = Dropout(0.4)(new_model)
new_model = Dense(CLASSES, activation='softmax')(new_model)

model = Model(inputs=base_model.input, outputs=new_model)

for layer in base_model.layers:
    layer.trainable = False
      
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

WIDTH = 640
HEIGHT = 245
BATCH_SIZE = 5

# data prep
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(
    '/home/luis/tcc/tcc/DEV/TKinterExample-master/dataset/',
    target_size=(HEIGHT, WIDTH),
		batch_size=BATCH_SIZE,
		class_mode='categorical')
    
validation_generator = validation_datagen.flow_from_directory(
    '/home/luis/tcc/tcc/DEV/TKinterExample-master/dataset_test/',
    target_size=(HEIGHT, WIDTH),
    batch_size=1,
    class_mode='categorical')


EPOCHS = 40
print(f'len train: {len(train_generator)}')
STEPS_PER_EPOCH = len(train_generator)
print(f'len test: {len(validation_generator)}')
VALIDATION_STEPS = len(validation_generator)

MODEL_FILE = 'InceptionV3.model'
start = time.time()
history = model.fit_generator(
    train_generator,
    epochs=EPOCHS,
    steps_per_epoch=STEPS_PER_EPOCH,
    validation_data=validation_generator,
    validation_steps=VALIDATION_STEPS)
  
model.save(MODEL_FILE)
stop = time.time()
print( f'Star: {start} stop: {stop} total{stop-start}')
print(history)
print('---------------')
print(history.history)
def plot_training(history):
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  loss = history.history['loss']
  val_loss = history.history['val_loss']
  epochs = range(len(acc))
  
  plt.plot(epochs, acc, 'r-',label='Treino')
  plt.plot(epochs, val_acc, 'g-',label='Validação')
  plt.title('Accurácia de treino e validação')
  
  plt.figure()
  plt.plot(epochs, loss, 'r-',label='Treino')
  plt.plot(epochs, val_loss, 'g-',label='Validação')
  plt.title('Loss de treino e validação')
  plt.show()
  
plot_training(history)
