import tensorflow as tf
import matplotlib.pyplot as plt
import time


def create_model_v2():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(64, activation='relu', input_shape=(784,)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))
    return model


def create_model_v3():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))
    return model


def train_model(model, x_train, y_train):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    start_time = time.time()
    model.fit(x_train, y_train, epochs=5, batch_size=32)
    end_time = time.time()

    training_time = end_time - start_time
    return training_time


# Load and preprocess your data
(x_train, y_train), (_, _) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape((60000, 784)) / 255.0

# Define the TensorFlow versions you want to compare
versions = ["2.0.0", "2.1.0", "2.2.0"]

# Lists to store training time values for each version
training_times = []

# Train models for each version and calculate training time
for version in versions:
    tf_version = tf.__version__

    try:
        # Set TensorFlow version
        tf.__version__ = version

        # Create the model
        if version == "2.0.0":
            model = create_model_v2()
        else:
            model = create_model_v3()

        # Train the model and calculate training time
        training_time = train_model(model, x_train, y_train)

        # Store the training time value
        training_times.append(training_time)

        print(f"Model trained with TensorFlow {version} - Training Time: {training_time} seconds")
    except:
        print(f"Error occurred while training the model with TensorFlow {version}")
    finally:
        # Restore the original TensorFlow version
        tf.__version__ = tf_version

# Plotting the training time values
plt.bar(versions, training_times)

# Setting labels and title
plt.xlabel('TensorFlow Version')
plt.ylabel('Training Time (seconds)')
plt.title('Comparison of Model Training Time Across TensorFlow Versions')

# Displaying the plot
plt.show()
