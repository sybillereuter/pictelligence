import gradio as gr
from clip_analyzer import generate

example_images = [
    "https://huggingface.co/datasets/s-reuter/sample-photos/resolve/main/kediler.jpg",
    "https://huggingface.co/datasets/s-reuter/sample-photos/resolve/main/swayambhu.jpg",
    "https://huggingface.co/datasets/s-reuter/sample-photos/resolve/main/chattydolls.jpg",
    "https://huggingface.co/datasets/s-reuter/sample-photos/resolve/main/self.jpg",
    "https://huggingface.co/datasets/s-reuter/sample-photos/resolve/main/birbs.jpg"
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
    iface.launch(ssr_mode=False)
