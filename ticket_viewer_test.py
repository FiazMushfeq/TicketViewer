from ticket_viewer_main import *
from ticket_viewer_utils import *
import requests
import unittest


subdomain = ''
email = ''
password = ''
num_tickets = 100


# This tests that the individual ticket information is correct
class test_GetIndividualTicket(unittest.TestCase):
    def test_tickets(self):
        data = requests.get('https://{}.zendesk.com/api/v2/tickets/count'.format(subdomain), auth = (email, password))
        current_num = data.json()['count']['value']
        for i in range(current_num):
            response = requests.get('https://{}.zendesk.com/api/v2/tickets/{}'.format(subdomain, current_num + 1), auth = (email, password)).json()
            test_response = get_individual_ticket(subdomain, email, password, current_num + 1).json()
            self.assertDictEqual(response, test_response)

# This tests to make sure that the responses from get_page() is correct
class test_GetPage(unittest.TestCase):
    def test_pages(self):
        base_url = 'https://{}.zendesk.com/api/v2/tickets.json?page[size]=25'.format(subdomain)
        base_response = requests.get(base_url, auth = (email, password)).json()
        while base_response['meta']['has_more'] is True:
            test_response = get_page(base_url, email, password)
            self.assertDictEqual(base_response, test_response)
            base_url = base_response['links']['next']
            base_response = requests.get(base_url, auth= (email, password)).json()



if __name__ == "__main__":
    unittest.main()
