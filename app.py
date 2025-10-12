import gradio as gr
from datasets import load_dataset
import os
from clip_analyzer import generate

dataset = load_dataset("s-reuter/sample-photos")
os.makedirs("sample_photos", exist_ok=True)

example_images = []

for i, item in enumerate(dataset["train"]):
    path = f"sample_photos/image_{i}.jpg"
    item['image'].save(path)
    example_images.append(path)


def process_image(image):
    tags = generate(image, 30)
    return ", ".join(tags)


iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil"),
    outputs=[
        gr.Textbox(label="Tags")
    ],
    title="Pictelligence :: AI Photo Tagger",
    description="Upload a photo to generate tags or use one of the examples below:",
    examples=example_images
)

if __name__ == "__main__":
    iface.launch(ssr_mode=False)
