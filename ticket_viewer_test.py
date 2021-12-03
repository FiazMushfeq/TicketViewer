from ticket_viewer_main import *
from ticket_viewer_utils import *
import requests
import unittest

subdomain = 'zccfiazmushfeq'
email = 'fiazmushfeq@live.com'
password = 'Hunt$92!!!'
num_tickets = 100

# The following tests the correctness of information that is not obvious or directly observable

# This tests that the individual ticket information is correct
class test_GetIndividualTicket(unittest.TestCase):
    def test_correctness_of_tickets(self):
        data = requests.get('https://{}.zendesk.com/api/v2/tickets/count'.format(subdomain), auth=HTTPBasicAuth(email, password))
        current_num = data.json()['count']['value']
        for i in range(current_num):
            response = requests.get('https://{}.zendesk.com/api/v2/tickets/{}'.format(subdomain, current_num + 1), auth=HTTPBasicAuth(email, password)).json()
            test_response = get_individual_ticket(subdomain, email, password, current_num + 1).json()
            self.assertDictEqual(response, test_response)

# This tests to make sure that the responses from get_page() is correct
class test_GetPage(unittest.TestCase):
    def test_correctness_of_pages(self):
        base_url = 'https://{}.zendesk.com/api/v2/tickets.json?page[size]=25'.format(subdomain)
        base_response = requests.get(base_url, auth=HTTPBasicAuth(email, password)).json()
        while base_response['meta']['has_more'] is True:
            test_response = get_page(base_url, email, password)
            self.assertDictEqual(base_response, test_response)
            base_url = base_response['links']['next']
            base_response = requests.get(base_url, auth=HTTPBasicAuth(email, password)).json()

# This tests the total number of tickets returned.
class TestTotalTicketCount(unittest.TestCase):
    # tests correctness in returning the number of tickets when deleting
    def test_correctness(self):
        test_num = total_ticket_count(subdomain, email, password)
        self.assertEqual(test_num, 100)
        # double-check that we indeed have 100 tickets
        response_num = requests.get('https://{}.zendesk.com/api/v2/tickets/count'.format(subdomain), auth=HTTPBasicAuth(email, password)).json()['count']['value']
        self.assertEqual(response_num, 100)
