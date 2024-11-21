import uuid
import cv2
import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from PIL import Image
import config
import inference


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from API"}


@app.post("/{style}")
def get_image(style: str, file: UploadFile = File(...)):
    image = np.array(Image.open(file.file))
    model = config.STYLE[style]
    output, resized = inference.inference(model,image)
    name = f"/storage/{str(uuid.uuid())}.jpg"
    cv2.imwrite(name, output)
    return {"name": name}


if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8080)
