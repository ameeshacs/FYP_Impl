import fastapi
import functions as f
import cv2
from PIL import Image
from collections import Counter
import numpy as np
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import base64
import skin_model as m
import requests
            

app = FastAPI()

origins = [
    "*"  # Allow requests from all origins
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the root endpoint
@app.post("/image")
async def image(data: dict):

    try:
        image_data = data["image"]
        decoded_image = base64.b64decode(image_data.split(",")[1])

        with open("saved.jpg","wb") as fi:
            fi.write(decoded_image)
      
        f.save_skin_mask("saved.jpg")
   
        ans = m.get_season("temp.jpg")
        os.remove("temp.jpg")
        os.remove("saved.jpg")
   
        if ans == 3:
            ans += 1
        elif ans == 0:
            ans = 3

        test = {'result': ans}
        encoded_data = base64.b64encode(str(test).encode('utf-8')).decode('utf-8')
 
        response = requests.post('http://localhost:3000/output',json={'encodedData':encoded_data})
        print(response.text) 
        return JSONResponse(content={"message":"complete"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="fail")


