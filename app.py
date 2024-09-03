import gradio as gr
import json
import requests
import os
import time
import re

#RARRI POST URL
URL = "http://10.11.0.232:8188/api/prompt"
OUTPUT_DIR = '//10.11.0.232/Users/Digital Experience/Downloads/ComfyUI_windows_portable_nvidia_cu118_or_cpu/ComfyUI_windows_portable/ComfyUI/output'


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


def generate_image():
    # Load workflow data from json file
    with open("workflow_api.json", "r",encoding="utf-8") as file_json:
        prompt = json.load(file_json)
    
    previous_image = get_image(OUTPUT_DIR)

    start_queue(prompt) 

    while True:
        latest_image = get_image(OUTPUT_DIR)
        if latest_image!= previous_image:
            return latest_image
        time.sleep(1)

ui = gr.Interface(fn=generate_image, inputs=[], outputs=['image'])

ui.launch()

