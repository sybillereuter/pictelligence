import unittest
import pandas as pd
import tags_preprocessor


class TestTagsPreprocessor(unittest.TestCase):

    def setUp(self):

        # Example data: preprocessor is tailored for Alamy data dump!
        self.test_row = pd.Series({
            'Filename': 'test_image.jpg',
            'ImageRef': 'xyz',
            'Caption': 'Underwater background; freshwater flora and fauna with water plants and small fish, on a sunny day with sunbeams and reflections on the water surface.',
            'Tags': 'aquatic,aquatic life,background,below the surface,diving,ecosystem,environment,fish,flora and fauna,fresh,freshwater,grass,green,green water,lake,lake life,lake water,landscape,life,light,marine,natural,nature,nature background,plant,pond,ray of light,reflection,reflection in water,school of fish,scuba diving,sea,seagrass,sun beams,sunrays,water background,wildlife animals,serene,peaceful',
            'License type': 'RF',
            'Username': 'AUTHOR',
            'Super Tags': 'lake fish,underwater flora and fauna,lake diving,underwater scene,underwater light rays,underwater background,underwater life,marine biology,freshwater fishing,freshwater fish',
            'Location': '',
            'Date taken': '03/09/2023',
            'Number of People': '0',
            'Model release': 'NA',
            'Is there property in this image?': 'N',
            'Property release': 'NA',
            'Primary category': 'Landscapes',
            'Secondary category': 'Animals and wildlife',
            'Image Type': 'Photograph',
            'Exclusive to Alamy': 'N',
            'Additional Info': '',
            'Status': 'On sale'
        })

        self.result = list(tags_preprocessor.extract_and_combine_tags_with_weights(self.test_row).keys())

    def test_all_tags_included(self):
        expected_tags = [
            'Aquatic', 'Aquatic Life', 'Background', 'Below the Surface', 'Diving',
            'Ecosystem', 'Environment', 'Fish', 'Flora and Fauna', 'Fresh',
            'Freshwater', 'Grass', 'Green', 'Green Water', 'Lake', 'Lake Life',
            'Lake Water', 'Landscape', 'Life', 'Light', 'Marine', 'Natural',
            'Nature', 'Nature Background', 'Plant', 'Pond', 'Ray of Light',
            'Reflection', 'Reflection in Water', 'School of Fish', 'Scuba Diving',
            'Sea', 'Seagrass', 'Sun Beams', 'Sunrays', 'Water Background',
            'Wildlife Animals', 'Serene', 'Peaceful'
        ]

        for expected_tag in expected_tags:
            with self.subTest(tag=expected_tag):
                self.assertIn(expected_tag, self.result, f"missing: '{expected_tag}'")

    def test_categories_included(self):
        expected_categories = ['Landscapes', 'Animals and Wildlife']

        for category in expected_categories:
            with self.subTest(category=category):
                self.assertIn(category, self.result, f"missing: '{category}'")

    def test_super_tags_included(self):
        expected_super_tags = [
            'Lake Fish', 'Underwater Flora and Fauna', 'Lake Diving',
            'Underwater Scene', 'Underwater Light Rays', 'Underwater Background',
            'Underwater Life', 'Marine Biology', 'Freshwater Fishing', 'Freshwater Fish'
        ]

        for super_tag in expected_super_tags:
            with self.subTest(super_tag=super_tag):
                self.assertIn(super_tag, self.result, f"missing: '{super_tag}'")

    def test_description_keywords_included(self):
        expected_description_keywords = [
            'Animals and Wildlife', 'Background Freshwater', 'Freshwater Flora', 'Flora Fauna', 'Fauna Water',
            'Water Plants', 'Plants Small', 'Small Fish', 'Fish Sunny', 'Sunny Day', 'Day Sunbeams',
            'Sunbeams Reflections', 'Reflections Water', 'Water Surface', 'Underwater Background Freshwater',
            'Background Freshwater Flora', 'Freshwater Flora Fauna', 'Flora Fauna Water', 'Fauna Water Plants',
            'Water Plants Small', 'Plants Small Fish', 'Small Fish Sunny', 'Fish Sunny Day', 'Sunny Day Sunbeams',
            'Day Sunbeams Reflections', 'Sunbeams Reflections Water', 'Reflections Water Surface', 'Underwater', 'Flora',
            'Fauna', 'Plants', 'Small', 'Sunny', 'Sunbeams', 'Reflections', 'Surface'
        ]

        for ngram in expected_description_keywords:
            with self.subTest(ngram=ngram):
                self.assertIn(ngram, self.result, f"missing: '{ngram}'")


if __name__ == '__main__':
    unittest.main()
