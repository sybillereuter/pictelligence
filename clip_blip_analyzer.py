import warnings
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, AutoProcessor, CLIPModel, CLIPProcessor


warnings.filterwarnings("ignore", message="Using the model-agnostic default `max_length`")

BLIP = "Salesforce/blip-image-captioning-base"
blip_model = BlipForConditionalGeneration.from_pretrained(BLIP)
blip_processor = AutoProcessor.from_pretrained(BLIP)

CLIP = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(CLIP)
clip_processor = CLIPProcessor.from_pretrained(CLIP)


def load_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tags = [line.strip() for line in file if line.strip()]
    return tags


tag_file_path = "tags.txt"
tag_list = load_tags(tag_file_path)


def generate_caption(image: Image.Image):
    inputs = blip_processor(image, return_tensors="pt")

    out = blip_model.generate(**inputs,
                              max_length=300,
                              num_beams=10,
                              do_sample=True,
                              temperature=1.2,
                              top_k=30,
                              top_p=0.9)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption


def generate_tags(image: Image.Image, description: str, num_tags=10, tags=tag_list):
    resized_image = image.resize((256, 256))
    inputs = clip_processor(
        text=[description] + tags,
        images=resized_image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = clip_model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)[0, 1:]
    top_tags = [tags[idx] for idx in probs.topk(num_tags).indices]

    return top_tags

