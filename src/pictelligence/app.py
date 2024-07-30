import gradio as gr

from clip_blip_analyzer import generate_caption, generate_tags


example_images = [
    "sample_photos/kediler.jpg",
    "sample_photos/swarm.jpg",
    "sample_photos/gijro.jpg"
]


def process_image(image):
    caption = generate_caption(image)
    tags = generate_tags(image, caption)
    return caption, tags


def process_and_save_image(image):
    caption, tags = process_image(image)
    return caption, tags


iface = gr.Interface(
    fn=process_and_save_image,
    inputs=gr.Image(type="pil"),
    outputs=[
        gr.Textbox(label="Description"),
        gr.Textbox(label="Tags")
    ],
    title="Pictelligence :: AI Photo Tagger",
    description="Upload a photo to generate a description and tags:",
    examples=example_images
)

if __name__ == "__main__":
    iface.launch()
