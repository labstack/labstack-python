import os
import unittest
from .client import Client


class TestCurrency(unittest.TestCase):
    def setUp(self):
        self.s = Client(os.getenv('KEY')).currency()

    def test_convert(self):
        response = self.s.convert({
            'amount': 10,
            'from': 'USD',
            'to': 'INR'
        })
        self.assertNotEqual(response['amount'], 0)

    def test_list(self):
        response = self.s.list({})
        self.assertNotEqual(len(response['currencies']), 0)

    def test_rates(self):
        response = self.s.rates({})
        self.assertNotEqual(len(response['rates']), 0)
