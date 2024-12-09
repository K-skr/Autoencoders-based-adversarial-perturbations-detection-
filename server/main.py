import os
from fastapi import FastAPI,Form,Request
from typing import Any, Dict,Annotated
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
import random
from crud import checkForValidLogin,createUser
import jwt
from functools import wraps
from auth import sign_jwt,decode_jwt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import pickle
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import io
from tensorflow.keras.utils import register_keras_serializable
import cv2
from zipfile import ZipFile

def load_images(image_directory):
    images = []

    for file_name in os.listdir(image_directory):
        if file_name.endswith(('.png', '.jpg', '.jpeg')): 
            image_path = os.path.join(image_directory, file_name)
            img = Image.open(image_path).resize((32, 32))  
            images.append(np.array(img))  

    images = np.array(images) / 255.0  # Normalize 
    print(f"Loaded {images.shape[0]} unlabelled images.")
    images.shape
    return images

@register_keras_serializable()
def SSIMLoss(y_true, y_pred):
    
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)

    if y_true.shape[-1] != y_pred.shape[-1]:
        if y_true.shape[-1] == 3:
            y_true = tf.image.rgb_to_grayscale(y_true)
        elif y_pred.shape[-1] == 3:
            y_pred = tf.image.rgb_to_grayscale(y_pred)

    return 1 - tf.reduce_mean(tf.image.ssim(y_true, y_pred, max_val=1.0))
def rgb_to_grayscale(images):
    return tf.image.rgb_to_grayscale(images)

def unzip(content):
    zip_output = []
    with ZipFile(io.BytesIO(content), 'r') as zip_file:
        sorted_names = sorted(zip_file.namelist())
        for file_name in sorted_names:
            
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                with zip_file.open(file_name) as file:
                    try:
                        
                        image = Image.open(io.BytesIO(file.read()))
                        numpy_image = np.array(image)
                        numpy_image = np.array(numpy_image) / 255.0 #normalize
                    
                        zip_output.append(numpy_image)

                        # print(f"File: {file_name}")
                        # print("Type:", type(numpy_image))
                        # print("Shape:", numpy_image.shape)
                        # print("Data type:", numpy_image.dtype)

                    except Exception as e:
                        print(f"Error processing file {file_name}: {e}")

    return zip_output  


normal_test_images = load_images('./test')
model  = tf.keras.models.load_model('./test.keras')


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def validateLogin(body: Dict[Any, Any]):
    user = checkForValidLogin(body["email"],body["password"])
    if(user == False):
        return {"success":False}
    else:
        token = sign_jwt(user[0])
        return {"success":True,"id":user[0],"token":token}
    

@app.post("/register")
async def validateReg(body: Dict[Any, Any]):
    # print(body)
    user = createUser(body["email"],body["password"])
    # print(user)
    if(user == False):
        return {"success":False}
    else:
        token = sign_jwt(user[0])
        return {"success":True,"id":user[0],"token":token}

@app.post("/model")
async def runModel(request: Request):
    # 
    form = await request.form()
    filename = form['file'].filename
    typeOfFile = filename.split('.')

    if(len(typeOfFile)<2):
        return {"success":False}

    typeOfFile = typeOfFile[len(typeOfFile)-1]



    if(typeOfFile=='png' or typeOfFile=='jpg' or typeOfFile == 'jpeg'):
        content = await form['file'].read()
        img = Image.open(io.BytesIO(content))
        img = np.array(img.resize((128, 128), Image.Resampling.LANCZOS))
        # img = preprocess_images(img)
        output = model.predict(img)
        return {"success":True,"output":output}
    elif typeOfFile == 'zip':
        content = await form['file'].read()
        # file_path = form['file'].filename  # Assuming this provides the path to the uploaded file

        zip_images = unzip(content)
        zip_images = rgb_to_grayscale(zip_images)
        # decoded_test = model.predict(normal_test_images)
        decoded_anomaly = model.predict(zip_images)
        value_a = SSIMLoss(normal_test_images[0], decoded_anomaly[0])
        n_v = float(value_a.numpy())
        if n_v> 0.2:
            return{"success":True,"anomaly":True,"reconstruction_error":n_v}
        else:
            return{"success":True,"anomaly":False,"reconstruction_error":n_v}
         
    return {"success":False,"msg":"File Type not supported"}