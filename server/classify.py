import tensorflow as tf
import numpy as np
import os
import zipfile
from urllib.request import urlretrieve
from io import BytesIO
from PIL import Image
from prepare_imagenet_data import preprocess_image_batch, undo_image_avg


def classify_image_from_bytes(image_raw_binary, labels_path='data/labels.txt', model_path='data/tensorflow_inception_graph.pb'):
    """
    Classifies an image from bytes format and returns the processed image and its predicted label.

    Args:
        image_bytes (bytes): Input image in bytes format.
        labels_path (str): Path to the labels file.
        model_path (str): Path to the frozen TensorFlow Inception model. Defaults to 'data/tensorflow_inception_graph.pb'.

    Returns:
        tuple: A tuple containing:
            - image (numpy.ndarray): Preprocessed image used for classification.
            - label (str): Predicted label of the image.
    """
    # Ensure model file exists
    if not os.path.isfile(model_path):
        print('Downloading Inception model...')
        if not os.path.exists('data'):
            os.makedirs('data')
        urlretrieve("https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip",
                    os.path.join('data', 'inception5h.zip'))
        # Unzipping the file
        with zipfile.ZipFile(os.path.join('data', 'inception5h.zip'), 'r') as zip_ref:
            zip_ref.extract('tensorflow_inception_graph.pb', 'data')

    # Load the frozen graph
    model = tf.io.read_file(model_path)
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(model.numpy())

    # Load labels
    labels = open(labels_path, 'r').read().split('\n')

    # Decode image bytes to a NumPy array
    image = Image.open(BytesIO(image_raw_binary)).convert("RGB")
    image_array = np.array(image)

    # Import graph to current session
    tf.compat.v1.reset_default_graph()
    with tf.compat.v1.Session() as sess:
        tf.import_graph_def(graph_def, name='')

        # Get input and output tensors
        input_tensor = sess.graph.get_tensor_by_name("input:0")
        output_tensor = sess.graph.get_tensor_by_name("softmax2_pre_activation:0")

        # Preprocess the input image
        image_numpy_data = preprocess_image_batch([image_array], img_size=(256, 256), crop_size=(224, 224), color_mode="rgb")

        # Run the model
        predictions = sess.run(output_tensor, feed_dict={input_tensor: np.reshape(image_numpy_data, (-1, 224, 224, 3))})
        predicted_label_index = np.argmax(predictions, axis=1).flatten()[0]

        # Get the corresponding label
        predicted_label = labels[predicted_label_index - 1].split(',')[0]  # Adjust for 1-based indexing in labels
        image_numpy_data = undo_image_avg(image_numpy_data[0])
        return image_numpy_data, predicted_label
