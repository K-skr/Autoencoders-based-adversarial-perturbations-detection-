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
model = load_model('./autoencoder.keras')
encoder_model = load_model('./encoder_model.keras')
with open('./kde_model.pkl', 'rb') as f:
    kde = pickle.load(f)
encoded_images_vector = np.load('./encoded_images_vector.npy', allow_pickle=True)
out_vector_shape = 512

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
        output = check_anomaly(content)
        return {"success":True,"output":output}

    return {"success":False,"msg":"File Type not supported"}

def check_anomaly(bimage):
    density_threshold = 320  # Set this value based on the above exercise
    reconstruction_error_threshold = 0.00736351  # Set this value based on the above exercise
    img = Image.open(io.BytesIO(bimage))
    img = np.array(img.resize((128, 128), Image.Resampling.LANCZOS))
    plt.imshow(img)
    img = img / 255.
    img = img[np.newaxis, :, :, :]
    encoded_img = encoder_model.predict([[img]])
    encoded_img = [np.reshape(img, (out_vector_shape)) for img in encoded_img]
    density = kde.score_samples(encoded_img)[0]

    reconstruction = model.predict([[img]])
    reconstruction_error = model.evaluate([reconstruction], [[img]], batch_size=1)[0]

    if density < density_threshold or reconstruction_error > reconstruction_error_threshold:
        return({"msg":"anamoly",
                "recon_error":reconstruction_error})

    else:
        return({"msg":"Not an anomaly",
                "recon_error":reconstruction_error})