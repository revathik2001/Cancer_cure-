
# Import necessary libraries
import os
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Set random seed for reproducibility
seed = 42
np.random.seed(seed)
# tf.random.set_seed(seed)
tf.random.set_random_seed(1)
random.seed(seed)

# Set the paths to your dataset
train_dir = "Dataset"
validation_dir = "Dataset"
model_save_path = "model_new.h5"  # Specify the path to save the trained model

# Define image dimensions and batch size
img_width, img_height = 150, 150
batch_size = 32

# Create data generators with data augmentation for the training set
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Rescale validation set
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Create generators for reading images from the directories
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(11, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Save the trained model
model.save(model_save_path)

# Evaluate the model
accuracy = model.evaluate(validation_generator)[1]
print(f"Validation Accuracy: {accuracy * 100:.2f}%")