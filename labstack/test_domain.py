import os
import unittest
from .client import Client


class TestDomain(unittest.TestCase):
    def setUp(self):
        self.s = Client(os.getenv('KEY')).domain()

    def test_dns(self):
        response = self.s.dns({
            'type': 'A',
            'domain': 'twilio.com'
        })
        self.assertNotEqual(len(response['records']), 0)

    def test_search(self):
        response = self.s.search({
            'q': 'twilio'
        })
        self.assertNotEqual(len(response['results']), 0)

    def test_status(self):
        response = self.s.status({
            'domain': 'twilio.com'
        })
        self.assertEqual(response['result'], 'unavailable')

    def test_whois(self):
        response = self.s.whois({
            'domain': 'twilio.com'
        })
        self.assertNotEqual(response['raw'], '')
