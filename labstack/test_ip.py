import os
import unittest
from .client import Client


class TestIP(unittest.TestCase):
    def setUp(self):
        self.s = Client(os.getenv('KEY')).ip()

    def test_ip(self):
        response = self.s.lookup({
            'ip': '96.45.83.67'
        })
        self.assertNotEqual(response['country'], '')
