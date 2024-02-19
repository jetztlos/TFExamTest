# From: https://www.tensorflow.org/tutorials/keras/text_classification_with_hub
## Setup
# ! pip install tensorflow-hub
# ! pip install tensorflow-datasets

import os
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)
print("GPU is", "available" if tf.config.list_physical_devices("GPU") else "NOT AVAILABLE")

## Download the IMDB dataset
# Split the training set into 60% and 40% to end up w/
# 15_000 ex. for training, 10_000 for validation, and 25_000 for testing.
train_data, validation_data, test_data = tfds.load(name="imdb_reviews",
                                                   split=('train[:60%]', 'train[60%:]', 'test'),
                                                   as_supervised=True)

## Explore the data
train_examples_batch, train_labels_batch = next(iter(train_data.batch(10)))
train_examples_batch

train_labels_batch

## Build the model
embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
hub_layer = hub.KerasLayer(embedding, input_shape=[],
                           dtype=tf.string, trainable=True)
hub_layer(train_examples_batch[:3])

model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1))

model.summary()

### Loss function, and optimizer
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])

## Train the model
history = model.fit(train_data.shuffle(10_000).batch(512),
                    epochs=10,
                    validation_data=validation_data.batch(512),
                    verbose=1)

## Evaluate the model
results = model.evaluate(test_data.batch(512),
                         verbose=2)
for name, value in zip(model.metrics_names, results):
    print("%s: %.3f" % (name, value))