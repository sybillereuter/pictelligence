import unittest
from PIL import Image
import clip_analyzer


class TestGenerateTags(unittest.TestCase):
    def setUp(self):
        image_path = "sample_photos/birbs.jpg"
        self.image = Image.open(image_path)
        self.number_of_tags = 30
        self.tags = clip_analyzer.generate(self.image, self.number_of_tags)

    def test_tags_not_empty(self):
        self.assertTrue(len(self.tags) > 0)

    def test_tags_contains_birds(self):
        self.assertIn("Birds", self.tags)

    @unittest.skip("Not deterministic; test is just here to make sure quality is not massively worse after a change.")
    def test_regression(self):
        old_tags = ['Flora and Fauna', 'Birds', 'Nature and Well-Being', 'Cooperation',
                    'Nature-Centric Living', 'Wildlife Photography', 'Nature Conservation',
                    'Mindfulness in Relationships', 'Romance', 'Connection to Nature',
                    'Belonging', 'Animals', 'Connection and Well-Being', 'Love as Inspiration',
                    'Compassion as Inspiration', 'Nature', 'Interpersonal Relationships',
                    'Conservation', 'Ecotherapy', 'Nature Photography', 'Animal Photography',
                    'Biodiversity', 'Wildlife Conservation', 'Conflict Resolution', 'Wildlife',
                    'Nature as Healer']
        self.assertCountEqual(old_tags, self.tags)


if __name__ == "__main__":
    unittest.main()
