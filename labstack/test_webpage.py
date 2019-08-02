import os
import unittest
from .client import Client


class TestWebpage(unittest.TestCase):
    def setUp(self):
        self.s = Client(os.getenv('KEY')).webpage()

    def test_image(self):
        response = self.s.image({
            'url': 'http://amazon.com'
        })
        self.assertNotEqual(response['image'], '')

    def test_pdf(self):
        response = self.s.pdf({
            'url': 'http://amazon.com'
        })
        self.assertNotEqual(response['pdf'], '')
