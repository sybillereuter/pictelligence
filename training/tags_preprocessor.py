import pandas as pd
import re
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from stopwords import ENGLISH_STOPWORDS, GERMAN_STOPWORDS

nltk.download('punkt')
nltk.download('punkt_tab')

all_stopwords = ENGLISH_STOPWORDS.union(GERMAN_STOPWORDS)


def extract_and_combine_tags_with_weights(row):
    tag_weights = {}

    if pd.notna(row['Tags']):
        for tag in normalize_tags(row['Tags'].split(',')):
            tag_weights[tag] = tag_weights.get(tag, 0) + 2

    if pd.notna(row['Super Tags']):
        for tag in normalize_tags(row['Super Tags'].split(',')):
            tag_weights[tag] = tag_weights.get(tag, 0) + 3

    if pd.notna(row['Primary category']):
        tag = normalize_tag(row['Primary category'])
        tag_weights[tag] = tag_weights.get(tag, 0) + 4
    if pd.notna(row['Secondary category']):
        tag = normalize_tag(row['Secondary category'].strip().upper())
        tag_weights[tag] = tag_weights.get(tag, 0) + 1

    if pd.notna(row['Caption']):
        for tag in normalize_tags(extract_ngrams_from_text(row['Caption'])):
            tag_weights[tag] = tag_weights.get(tag, 0) + 1

    return tag_weights


def extract_ngrams_from_text(text):
    if pd.isna(text):
        return []

    text = re.sub(r'[^\w\s-]', '', str(text).lower())

    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in ENGLISH_STOPWORDS and len(token) > 2]

    all_ngrams = []

    if len(filtered_tokens) >= 2:
        bigrams = [' '.join(bigram) for bigram in ngrams(filtered_tokens, 2)]
        all_ngrams.extend(bigrams)

    if len(filtered_tokens) >= 3:
        trigrams = [' '.join(trigram) for trigram in ngrams(filtered_tokens, 3)]
        all_ngrams.extend(trigrams)

    important_words = [token for token in filtered_tokens if len(token) > 3]
    all_ngrams.extend(important_words)

    return all_ngrams


def normalize_tags(tag_list):
    normalized_tags = []

    for tag in tag_list:
        normalized_tags.append(normalize_tag(tag))

    return normalized_tags


def normalize_tag(tag):
    if ' ' in tag:
        words = tag.split(' ')
        normalized_words = []

        for word in words:
            if word.lower() in all_stopwords:
                normalized_words.append(word.lower())
            else:
                normalized_words.append(word.capitalize())

        normalized_tag = ' '.join(normalized_words)
    else:
        if tag.lower() in all_stopwords:
            normalized_tag = tag.lower()
        else:
            normalized_tag = tag.capitalize()
    return normalized_tag
