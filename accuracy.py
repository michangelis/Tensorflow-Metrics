import tensorflow as tf
import matplotlib.pyplot as plt


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


def train_and_evaluate_model(model, x_train, y_train, x_test, y_test):
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5, batch_size=32)

    _, accuracy = model.evaluate(x_test, y_test)

    return accuracy


# Load and preprocess your data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape((60000, 784)) / 255.0
x_test = x_test.reshape((10000, 784)) / 255.0

# Define the TensorFlow versions you want to compare
versions = ["2.0.0", "2.1.0", "2.2.0"]

# Lists to store accuracy values for each version
accuracy_values = []

# Train and evaluate models for each version
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

        # Train and evaluate the model
        accuracy = train_and_evaluate_model(model, x_train, y_train, x_test, y_test)

        # Store the accuracy value
        accuracy_values.append(accuracy)

        print(f"Model trained with TensorFlow {version} - Accuracy: {accuracy}")
    except:
        print(f"Error occurred while training and evaluating the model with TensorFlow {version}")
    finally:
        # Restore the original TensorFlow version
        tf.__version__ = tf_version

# Plotting the accuracy values
plt.plot(versions, accuracy_values, marker='o')

# Setting labels and title
plt.xlabel('TensorFlow Version')
plt.ylabel('Accuracy')
plt.title('Comparison of Model Accuracy Across TensorFlow Versions')

# Displaying the plot
plt.show()
