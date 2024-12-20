import numpy as np
import os
from PIL import Image
from io import BytesIO
import base64
#from scipy.misc import imread, imresize
from matplotlib import pyplot as plt
import io
CLASS_INDEX = None
CLASS_INDEX_PATH = 'https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json'

def preprocess_image(img, target_size=(128, 128)):
    images = []
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize image to target size
    img = img.resize(target_size)
    # Convert image to NumPy array and normalize to [0, 1]
    img_array = np.array(img) / 255.0
    images.append(img_array)
    images_array = np.array(images)

    return images_array
def mean_squared_error(image1, image2):
    # Flatten the images to 1D arrays and compute the MSE
    diff = image1 - image2
    mse = np.mean(np.square(diff))  # MSE calculation
    return mse
def preprocess_image_batch(image_arr, img_size=None, crop_size=None, color_mode="rgb", out=None):
    img_list = []

    for img_a in image_arr:
        img = Image.fromarray(img_a).convert('RGB')
        img = np.array(img)
        if img_size:
            img = Image.fromarray(img).resize(img_size, Image.Resampling.LANCZOS)
            img = np.array(img)
        img = img.astype('float32')
        # We normalize the colors (in RGB space) with the empirical means on the training set
        img[:, :, 0] -= 123.68
        img[:, :, 1] -= 116.779
        img[:, :, 2] -= 103.939
        # We permute the colors to get them in the BGR order
        # if color_mode=="bgr":
        #    img[:,:,[0,1,2]] = img[:,:,[2,1,0]]

        if crop_size:
            img = img[(img_size[0] - crop_size[0]) // 2:(img_size[0] + crop_size[0]) // 2, (img_size[1]-crop_size[1])//2:(img_size[1]+crop_size[1])//2, :]

        img_list.append(img)

    try:
        img_batch = np.stack(img_list, axis=0)
    except:
        raise ValueError('when img_size and crop_size are None, images'
                ' in image_paths must have the same shapes.')

    if out is not None and hasattr(out, 'append'):
        out.append(img_batch)
    else:
        return img_batch

def undo_image_avg(img):
    img_copy = np.copy(img)
    img_copy[:, :, 0] = img_copy[:, :, 0] + 123.68
    img_copy[:, :, 1] = img_copy[:, :, 1] + 116.779
    img_copy[:, :, 2] = img_copy[:, :, 2] + 103.939
    return img_copy

def create_imagenet_npy(path_train_imagenet, len_batch=10000):

    # path_train_imagenet = '/datasets2/ILSVRC2012/train';

    sz_img = [224, 224]
    num_channels = 3
    num_classes = 1000

    im_array = np.zeros([len_batch] + sz_img + [num_channels], dtype=np.float32)
    num_imgs_per_batch = int(len_batch / num_classes)

    dirs = [x[0] for x in os.walk(path_train_imagenet)]
    dirs = dirs[1:]

    # Sort the directory in alphabetical order (same as synset_words.txt)
    dirs = sorted(dirs)

    it = 0
    Matrix = [0 for x in range(1000)]

    for d in dirs:
        for _, _, filename in os.walk(os.path.join(path_train_imagenet, d)):
            Matrix[it] = filename
        it = it+1


    it = 0
    # Load images, pre-process, and save
    for k in range(num_classes):
        for u in range(num_imgs_per_batch):
            print('Processing image number ', it)
            path_img = os.path.join(dirs[k], Matrix[k][u])
            image = preprocess_image_batch([path_img],img_size=(256,256), crop_size=(224,224), color_mode="rgb")
            im_array[it:(it+1), :, :, :] = image
            it = it + 1

    return im_array

def img_to_base64(img_array):
    # Convert NumPy array to a PIL image
    img_array = np.uint8(img_array)

    # Convert NumPy array to a PIL image
    image = Image.fromarray(img_array)
    
    # Create a BytesIO buffer to hold the image in memory
    buffered = BytesIO()
    
    # Save the image as PNG (you can change to 'JPEG' or other formats)
    image.save(buffered, format="PNG")
    
    # Get the base64 encoded string
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_base64

import matplotlib.pyplot as plt
import numpy as np

def create_image_with_labels(image1, label1, image2, label2):
    # Load the third image from the folder
    image3 = Image.open('./data/PERTURBATIONS_ADDED.png').convert("RGB")
    image3 = np.array(image3)

    # Create a new figure with three columns and adjust the width ratios
    fig, axs = plt.subplots(1, 3, figsize=(18, 6), gridspec_kw={'width_ratios': [3, 1, 3]})

    # Display the first image
    axs[0].imshow(image1.astype(dtype='uint8'))
    axs[0].set_title(label1, fontsize=25)  # Increased title font size
    axs[0].axis('off')  # Hide axes

    # Display the second image (middle image)
    axs[1].imshow(image3.astype(dtype='uint8'))
    axs[1].set_title('')  # Increased title font size
    axs[1].axis('off')  # Hide axes

    # Display the third image
    axs[2].imshow(image2.astype(dtype='uint8'))
    axs[2].set_title(label2, fontsize=25)  # Increased title font size
    axs[2].axis('off')  # Hide axes

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Draw the canvas to ensure the plot is rendered
    fig.canvas.draw()

    # Retrieve the width and height of the canvas
    width, height = fig.canvas.get_width_height()

    # Extract the RGBA buffer from the canvas
    buffer = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)

    # Reshape the buffer to an array of shape (height, width, 4)
    buffer = buffer.reshape((height, width, 4))

    # Convert from ARGB to RGBA
    buffer = buffer[:, :, [1, 2, 3, 0]]

    # Close the figure to free up memory
    plt.close(fig)

    return buffer