import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds

print(tf.__version__)

# $ googleimagesdownload --keywords 'jack russel terrier dog' \
# --limit 100 \
# --size medium \
# --chromedriver ./chromedriver \
# --format jpg

# download dataset
import pathlib
dataset_url = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"
archive = tf.keras.utils.get_file(origin=dataset_url, extract=True)
data_dir = pathlib.Path(archive).with_suffix('')

# total imgs
image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

#load using keras utility, define params
batch_size = 32
img_height = 180
img_width = 180

# validation split
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split = 0.2,
  subset = "training",
  seed = 123,
  img_size = (img_height, img_width),
  batch_size = batch_size)

  val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split = 0.2,
  subset = "validation",
  seed = 123,
  img_size = (img_height, img_width),
  batch_size = batch_size)

  class_names = train_ds.class_names
  print(class_names)

  #change rgb channels ([0, 255] to [0, 1] )
  normalization_layer = tf.keras.layers.Rescaling(1./255)

# creating Sequential model
#   model = keras.Sequential(
#     [
#         layers.Dense(2, activation="relu"),
#         layers.Dense(3, activation="relu"),
        
#     ]
# )

# pooling layers
num_classes = 4

model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

# see accuracy, loss in results
model.compile(
  optimizer='adam',
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  #validation accuracy 
  metrics=['accuracy'])

#epochs: iterations of training
model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=10
)

# ex. results
# Epoch 1/10
# 92/92 [==============================] - 14s 23ms/step - loss: 1.2346 - accuracy: 0.4816 - val_loss: 1.0334 - val_accuracy: 0.5699
# Epoch 2/10
# 92/92 [==============================] - 2s 20ms/step - loss: 1.0344 - accuracy: 0.5671 - val_loss: 0.9510 - val_accuracy: 0.6125
# Epoch 3/10
# 92/92 [==============================] - 2s 20ms/step - loss: 0.7755 - accuracy: 0.6702 - val_loss: 0.9037 - val_accuracy: 0.6381
