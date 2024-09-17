import unittest
from PIL import Image
import clip_analyzer


class TestGenerateTags(unittest.TestCase):
    def setUp(self):
        image_path = "sample_photos/birbs.jpg"
        self.image = Image.open(image_path)
        self.number_of_tags = 30
        self.tags = clip_analyzer.generate(self.image, self.number_of_tags)
        print(self.tags)

    def test_tags_not_empty(self):
        self.assertTrue(len(self.tags) > 0)

    def test_tags_contains_birds(self):
        self.assertIn("Birds", self.tags)


if __name__ == "__main__":
    unittest.main()
