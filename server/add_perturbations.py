import numpy as np
import matplotlib.pyplot as plt
from prepare_imagenet_data import preprocess_image_batch, undo_image_avg
from PIL import Image
import numpy as np
from PIL import Image
import io

def add_perturbation(img):
    # Load the universal perturbation       
    file_perturbation = 'data/universal.npy'
    v = np.load(file_perturbation)
    
    # Convert the input image bytes to a PIL Image
    image = Image.open(io.BytesIO(img)).convert("RGB")
    image_array = np.array(image)

    # Preprocess the test image
    image_original = preprocess_image_batch([image_array], img_size=(256, 256), crop_size=(224, 224), color_mode="rgb")

    # Clip the perturbation to fit valid pixel range
    clipped_v = np.clip(undo_image_avg(image_original[0, :, :, :] + v[0, :, :, :]), 0, 255) - np.clip(
        undo_image_avg(image_original[0, :, :, :]), 0, 255)

    # Create the perturbed image
    image_perturbed = image_original + clipped_v[None, :, :, :]

    # Undo preprocessing for visualization
    perturbed_display = undo_image_avg(image_perturbed[0, :, :, :]).astype(dtype='uint8')

    # Convert the numpy array to a PIL Image
    perturbed_display = Image.fromarray(perturbed_display)
    perturbed_display.save(r"C:\Users\ASUS\Desktop\perturbed.png")
    # Create a BytesIO object to hold the image data
    img_byte_arr = io.BytesIO()

    # Save the image to the BytesIO object in the desired format (e.g., 'PNG')
    perturbed_display.save(img_byte_arr, format='PNG')

    # Retrieve the byte data from the BytesIO object
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr

