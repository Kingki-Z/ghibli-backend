import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_VERSION = os.getenv("REPLICATE_VERSION")

@app.post("/ghibli")
async def ghibli_style(image: UploadFile = File(...)):
    image_bytes = await image.read()
    base64_image = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode()

    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }

# trigger deploy
    json_data = {
        "version": REPLICATE_VERSION,
        "input": {
            "image": base64_image,
            "prompt": "Ghibli anime style photo"
        }
    }

    response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=json_data)
    return response.json()

