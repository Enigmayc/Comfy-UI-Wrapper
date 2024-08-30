import gradio as gr


def generate_image():
    pass

ui = gr.Interface(fn=generate_image, inputs=[], outputs=['image'])

ui.launch()