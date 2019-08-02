import os
import unittest
from .client import Client


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.s = Client(os.getenv('KEY')).email()

    def test_verify(self):
        response = self.s.verify({
            'email': 'jon@labstack.com'
        })
        self.assertEqual(response['result'], 'deliverable')
