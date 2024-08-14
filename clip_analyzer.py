import warnings
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import clean_tags
import tag_provider


warnings.filterwarnings("ignore", message="Using the model-agnostic default `max_length`")


CLIP = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(CLIP)
clip_processor = CLIPProcessor.from_pretrained(CLIP)


def generate(image: Image.Image, num_tags=10):
    cats = generate_tags(image, "", 3, tag_provider.categories)

    tags = [
        tag
        for cat in cats
        for tag in generate_tags(
            image,
            "",
            3 if len(tag_provider.tags_inventory.get(cat, {}).values()) < 50 else 5,
            [tag for tags in tag_provider.tags_inventory.get(cat, {}).values() for tag in tags]
        )
    ]
    tags += cats

    unique_tags = {clean_tags.normalize_phrase(tag.strip()) for tag in tags if tag.strip()}
    singular_tags = set(clean_tags.filter_singular_phrases(unique_tags))

    if len(singular_tags) < num_tags:
        additional_tags = generate_tags(image, "", num_tags - len(singular_tags), tag_provider.generic_tags)
        singular_tags.update(clean_tags.normalize_phrase(tag.strip()) for tag in additional_tags if tag.strip())

    return list(clean_tags.filter_singular_phrases(singular_tags))


def generate_tags(image: Image.Image, description: str, num_tags=10, tags=tag_provider.generic_tags):
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

