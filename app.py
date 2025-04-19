import gradio as gr
from clip_analyzer import generate

example_images = [
    "sample_photos/kediler.jpg",
    "sample_photos/swayambhu.jpg",
    "sample_photos/chattydolls.jpg",
    "sample_photos/self.jpg",
    "sample_photos/birbs.jpg"
]


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
    iface.launch()
