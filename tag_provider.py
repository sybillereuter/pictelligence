import json
import os

TAGS_DIR = "tags"

file_names = {
    "Abstract": [
        "abstract.txt"
    ],
    "Aerial": [
        "aerial.txt"
    ],
    "Animals": [
        "animals.txt",
        "animals_names.txt",
        "wildlife.txt",
        "pets.txt"
    ],
    "Architecture": [
        "architecture.txt"
    ],
    "Black and White": [
        "blackandwhite.txt"
    ],
    "Business": [
        "business.txt"
    ],
    "Candid": [
        "candid.txt"
    ],
    "Cultural": [
        "cultural.txt",
        "religion.txt"
    ],
    "Documentary": [
        "documentary.txt"
    ],
    "Events": [
        "events.txt"
    ],
    "Fashion": [
        "fashion.txt"
    ],
    "Fine Art": [
        "fineart.txt"
    ],
    "Food": [
        "food.txt"
    ],
    "Historical Sites": [
        "historicalsites.txt",
        "architecture.txt"
    ],
    "Industry": [
        "industry.txt"
    ],
    "Landscapes": [
        "landscapes.txt",
        "scenery_descriptors.txt",
        "weather_descriptors.txt",
        "nature.txt"
    ],
    "Lost Places": [
        "lostplaces.txt"
    ],
    "Macro": [
        "macro.txt"
    ],
    "Nature": [
        "nature.txt",
        "weather_descriptors.txt"
    ],
    "Night": [
        "night.txt"
    ],
    "Pets": [
        "pets.txt"
    ],
    "Portraits": [
        "portraits.txt"
    ],
    "Seascapes": [
        "seascapes.txt"
    ],
    "Sports": [
        "sports.txt",
        "water_sports.txt"
    ],
    "Still Life": [
        "stillife.txt"
    ],
    "Technology": [
        "technology.txt"
    ],
    "Travel": [
        "travel.txt",
        "place_names.txt",
        "landscapes.txt",
        "scenery_descriptors.txt"
    ],
    "Underwater": [
        "underwater.txt",
        "fish.txt",
        "water_sports.txt"
    ],
    "Urban": [
        "urban.txt"
    ],
    "Vehicles": [
        "vehicles.txt"
    ],
    "Wildlife": [
        "wildlife.txt",
        "animals.txt",
        "animals_names.txt"
    ]
}

generic = [
    "generic_mythemes.txt",
    "generic_large.txt",
    "meta_photography.txt",
    "positive_concepts.txt"
]


def load_tags():
    return {
        category: {
            filename: read_tags(os.path.join(TAGS_DIR, filename))
            for filename in filenames
        }
        for category, filenames in file_names.items()
    }


def load_generic_tags():
    return [
        tag
        for filename in generic
        for tag in read_tags(os.path.join(TAGS_DIR, filename))
    ]


def read_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


tags_inventory = load_tags()
generic_tags = load_generic_tags()
categories_file_path = "tags/categories.txt"
categories = read_tags(categories_file_path)

