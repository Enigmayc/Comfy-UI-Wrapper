import gradio as gr
import json
import requests
import os
import time
from PIL import Image
import numpy as np

#RARRI POST URL
URL = "http://10.11.0.232:8188/api/prompt"
OUTPUT_DIR = '//10.11.0.232/Users/Digital Experience/Downloads/ComfyUI_windows_portable_nvidia_cu118_or_cpu/ComfyUI_windows_portable/ComfyUI/output'
INPUT_DIR = '//10.11.0.232/Users/Digital Experience/Downloads/ComfyUI_windows_portable_nvidia_cu118_or_cpu/ComfyUI_windows_portable/ComfyUI/input/input.png'
INPUT_DIR_REF = '//10.11.0.232/Users/Digital Experience/Downloads/ComfyUI_windows_portable_nvidia_cu118_or_cpu/ComfyUI_windows_portable/ComfyUI/input/refer.png'


#generated image from rarri
def get_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', 'jpeg'))]
    image_files.sort(key = lambda x : os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files [-1]) if image_files else None
    return latest_image


#create a post request
def start_queue(prompt_workflow):
    p = {"prompt" : prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data = data)

def generate_image(upload_image_1, upload_image_2):
    # Convert the uploaded image to a PIL image if necessary
    if isinstance(upload_image_1, np.ndarray):
        upload_image_1 = Image.fromarray(upload_image_1)

    # Resize the image to match the input requirements (assuming 512x512)
    min_side = min(upload_image_1.size)
    scale_factor = 512 / min_side
    new_side = (round(upload_image_1.size[0] * scale_factor), round(upload_image_1.size[1] * scale_factor))
    resized_image_1 = upload_image_1.resize(new_side)

    # Save the resized image to the input directory
    resized_image_1.save(INPUT_DIR)

    if isinstance(upload_image_2, np.ndarray):
        upload_image_2 = Image.fromarray(upload_image_2)

    # Resize the image to match the input requirements (assuming 512x512)
    min_side = min(upload_image_2.size)
    scale_factor = 512 / min_side
    new_side = (round(upload_image_2.size[0] * scale_factor), round(upload_image_2.size[1] * scale_factor))
    resized_image_2 = upload_image_2.resize(new_side)

    # Save the resized image to the input directory
    resized_image_2.save(INPUT_DIR_REF)

    # Load workflow data from JSON file
    with open("imgtoimg_api.json", "r", encoding="utf-8") as file_json:
        prompt = json.load(file_json)
        prompt['14']['inputs']['image'] = INPUT_DIR 
        prompt['18']['inputs']['image'] = INPUT_DIR_REF # Set the path to the uploaded image


    previous_image = get_image(OUTPUT_DIR)

    start_queue(prompt) 

    while True:
        latest_image = get_image(OUTPUT_DIR)
        if latest_image!= previous_image:
            return latest_image
        time.sleep(1)

ui = gr.Interface(fn=generate_image, inputs=['image', 'image'], outputs=['image'])

ui.launch()

