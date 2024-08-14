import os
import unicodedata
from pathlib import Path
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


nltk_data_path = '/app/nltk_data'
os.makedirs(nltk_data_path, exist_ok=True)

nltk.download('punkt', download_dir='/app/nltk_data')
nltk.download('averaged_perceptron_tagger', download_dir='/app/nltk_data')
nltk.download('wordnet', download_dir='/app/nltk_data')

nltk.data.path.append('/app/nltk_data')

lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(tag):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def normalize_phrase(phrase):
    phrase = unicodedata.normalize('NFKD', phrase)
    return phrase.replace("’", "'").replace("`", "'")


def normalize_and_lemmatize(phrase):
    normalized_phrase = normalize_phrase(phrase)
    words = normalized_phrase.split()
    singular_words = [
        lemmatizer.lemmatize(word.lower(), get_wordnet_pos(tag))
        for word, tag in nltk.pos_tag(words)
    ]
    return ' '.join(singular_words)


def filter_singular_phrases(phrases):
    original_to_singular = {}

    for phrase in phrases:
        singular_phrase = normalize_and_lemmatize(phrase)
        original_to_singular.setdefault(singular_phrase, phrase)

    return list(original_to_singular.values())


def clean_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        tags = file.readlines()
    unique_tags = set(normalize_phrase(tag.strip()) for tag in tags if tag.strip())
    singular_tags = filter_singular_phrases(unique_tags)

    with open(output_file, 'w', encoding='utf-8') as file:
        for tag in sorted(singular_tags):
            file.write(f"{tag}\n")


def clean_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt') and not filename.endswith('-clean.txt'):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename.replace('.txt', '-clean.txt'))
            clean_tags(input_file, output_file)


def cleanup_directory(directory):
    dir_path = Path(directory)

    for file_path in dir_path.iterdir():
        if file_path.suffix != '-clean.txt':
            file_path.unlink()

    for file_path in dir_path.glob('*-clean.txt'):
        new_file_path = file_path.with_name(file_path.stem.replace('-clean', '') + '.txt')
        if new_file_path.exists():
            new_file_path.unlink()

        file_path.rename(new_file_path)
