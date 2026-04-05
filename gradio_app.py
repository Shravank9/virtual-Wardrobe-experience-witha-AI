import gradio as gr
import os
import time
from PIL import Image

# Function to run the virtual try-on process
def run_virtual_try_on(person_image, cloth_image):
    # Save uploaded images to the static folder
    person_image_path = "static/origin_web.jpg"
    cloth_image_path = "static/cloth_web.jpg"
    person_image.save(person_image_path)
    cloth_image.save(cloth_image_path)

    # Run the main processing script
    try:
        start_time = time.time()
        os.system("python3 main.py")
        processing_time = time.time() - start_time

        # Check if the result image was generated
        result_image_path = "static/finalimg.png"
        if os.path.exists(result_image_path):
            result_image = Image.open(result_image_path)
            return result_image, f"Processing time: {processing_time:.1f} seconds"
        else:
            return None, "Error: No output generated"
    except Exception as e:
        return None, f"Error during processing: {str(e)}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 👗 Virtual Clothing Try-On")
    gr.Markdown("Upload a photo of yourself and a clothing item to see how it looks!")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Step 1: Upload Person Image")
            person_image = gr.Image(label="Person Image", type="pil")
        with gr.Column():
            gr.Markdown("### Step 2: Upload Clothing Image")
            cloth_image = gr.Image(label="Clothing Image", type="pil")

    with gr.Row():
        run_button = gr.Button("Run Virtual Try-On", variant="primary")

    with gr.Row():
        result_image = gr.Image(label="Virtual Try-On Result")
        processing_time = gr.Textbox(label="Processing Time")

    # Link the button to the function
    run_button.click(
        fn=run_virtual_try_on,
        inputs=[person_image, cloth_image],
        outputs=[result_image, processing_time]
    )

# Launch the Gradio app
demo.launch()