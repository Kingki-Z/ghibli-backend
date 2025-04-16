import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI()

# 添加跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量读取 Replicate Token 和模型版本
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_VERSION = os.getenv("REPLICATE_VERSION")

@app.post("/ghibli")
async def ghibli_style(image: UploadFile = File(...)):
    try:
        # 读取上传的图片为 base64 格式
        image_bytes = await image.read()
        base64_image = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode()

        # 设置请求头
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json",
        }

        # 构建请求体
        json_data = {
            "version": REPLICATE_VERSION,
            "input": {
                "image": base64_image,
                "prompt": "Ghibli anime style photo"
            }
        }

        # 向 Replicate 发送 POST 请求
        response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=json_data)
        
        # 打印返回内容到日志中（方便 Render Logs 查看）
        print("Replicate response:", response.status_code, response.text)

        # 返回结果
        return response.json()

    except Exception as e:
        # 捕获并打印错误
        print("Error occurred:", str(e))
        return {"error": str(e)}
