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
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
# import pickle
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import io
from tensorflow.keras.utils import register_keras_serializable
import cv2
from zipfile import ZipFile
import zipfile
import base64
from classify import classify_image_from_bytes
from prepare_imagenet_data import img_to_base64, create_image_with_labels, preprocess_image, mean_squared_error
from add_perturbations import add_perturbation


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
# this is for demo
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
        perturbed_image = add_perturbation(content)
        #returns numpy array
        orig_img, o_label = classify_image_from_bytes(content)
        perturb_img, p_label = classify_image_from_bytes(perturbed_image)
        # create a plot of the two images
        plt_img = create_image_with_labels(orig_img,o_label, perturb_img,p_label)
        # img = preprocess_images(img)
        img1_64 = img_to_base64(plt_img)
        return {"success":True,"image":img1_64}
    elif typeOfFile == 'zip':
        return None
         
    return {"success":False,"msg":"File Type not supported"}

@app.post("/model1")
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
        input_image = Image.open(io.BytesIO(content))
        autoencoder = tf.keras.models.load_model('./data/autoencoder.keras')
        input_image = preprocess_image(input_image)
        reconstructed_image = autoencoder.predict(input_image)
        mse_value = mean_squared_error(reconstructed_image, input_image)
        if mse_value>0.003:
            return {"success":True,"perturbed":True,"recon_error":mse_value}
        else:
            return {"success":True,"perturbed":False,"recon_error":mse_value}
    elif typeOfFile == 'zip':
        return None
         
    return {"success":False,"msg":"File Type not supported"}