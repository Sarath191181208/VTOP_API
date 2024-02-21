import base64
import os 
import io
import json 
import numpy as np 
from PIL import Image

curr_dir = os.path.dirname(__file__)

# Loading the ML Model 
WEIGHTS_FILE_PATH = os.path.join(curr_dir, "weights.json")
with open(WEIGHTS_FILE_PATH, "r") as f:
    model_config = json.load(f)

weights = np.array(model_config["weights"])
biases = np.array(model_config["biases"])

def partition_img(img: np.ndarray) -> list[np.ndarray]:
    parts = [] 
    for i in range(6):
        x1 = (i + 1) * 25 + 2
        y1 = 7 + 5 * (i % 2) + 1
        x2 = (i + 2) * 25 + 1
        y2 = 35 - 5 * ((i + 1) % 2)
        # select the bounding box 
        part = img[y1:y2, x1:x2]
        parts.append(part)
    return parts

def convert_to_abs_bw(img: np.ndarray) -> np.ndarray:
    avg = np.sum(img)
    avg /= 24 * 22
    return np.where(img > avg, 0, 1)

def solve_captcha(captcha: str) -> str: 
    img = _str_to_img(captcha)
    # img = convert_to_abs_bw(img)
    img = partition_img(img)
    return _solve_captcha_ml(img)

def _solve_captcha_ml(img: list[np.ndarray]) -> str:
    LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    captcha = ""
    for single_letter in img:
        dw_img = convert_to_abs_bw(single_letter)
        dw_img = dw_img.flatten()
        x = np.dot(dw_img, weights) + biases
        x = np.exp(x)
        captcha += LETTERS[np.argmax(x)]
    return captcha

def _str_to_img(src: str) -> np.ndarray:
    # decoding the base64 string i.e string -> bytes -> image
    im = base64.b64decode(src)
    img = Image.open(io.BytesIO(im)).convert("L")
    # img.save("./_test/saves/img.png")
    img = np.array(img)
    return img
