import requests
import math
from ticket_viewer_utils import *


# get a single ticket for a user's account
def get_single_ticket(result, ticket_id):

    check = False
    print('\n')
    
    # print the ticket # and bold it
    print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - -  ')
    print("Showing details for " + "Zendesk Ticket #" + ticket_id )
    print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - -  ')
    
    # print each property and the value for the ticket
    for r in result['ticket']:
        print(r + ':', result['ticket'][r])
    print('\n')

    # GET ticket was successful, return True
    check = True
    return check


# Get all tickets for the user
def get_all_tickets(url, user, password, total_tickets):

    check = False
    count = 0

    print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - ')
    print('You are viewing your first 25 Zendesk Tickets')
    print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - ')
        
    # Display first 25 tickets
    first_page_url = url + '/api/v2/tickets.json?page[size]=25'
    current_url = first_page_url
    first_page_result = call_zendesk_api(first_page_url, user, password)
    current_page_result = first_page_result
    # determine the first and last page that one can page through
    current_page_number = 1
    last_page_number = int(math.ceil(total_tickets / 25))
    list_tickets(current_page_result, current_page_number, last_page_number)

    while True:
        # User can press N or n to continue seeing results from next page, or any other key to quit
        command = input("\nPlease enter N/n to see the next page or any other key to quit: ")

        # exit out of the CLI
        if (command != 'n' and command != 'N'):
            print('Thank you for using Zendesk Ticket Viewer. You will be returning to the main menu.')
            break

        # list the next page of tickets
        else:
            if current_page_number == last_page_number:
                print('This is the last page! Returning to Main menu!')
                break
            else:
                current_url = current_page_result['links']['next']
                current_page_result = call_zendesk_api(current_url, user, password)
                current_page_number += 1
                list_tickets(current_page_result, current_page_number, last_page_number)



    # GET all tickets was successful, return True
    check = True
    return check



# A ticket viewer program for Zendesk accounts (Get all or Get single)
def main():
    print("--------------------------------")
    print("Welcome to Zendesk Ticket Viewer ")
    print("--------------------------------")
    
    # Getting user credentials for making API calls to Zendesk Ticket Viewer
    subdomain, user, password = get_user_cred()
   
    user_entry = input("Type 'menu' to view options or 'quit' to exit: ")
    # keep getting input if user does not type one of the two valid options
    while user_entry != 'menu' and res != 'quit':
        print('Invalid choice, please try again.')
        res = input("Type 'menu' to view options or 'quit' to exit: ")

    if user_entry == 'menu':
        
        # keep presenting options for user to view all tickets or single ticket 
        # until they enter 'quit'
        while True:
            user_options()
            choice = input()

            # In case of invalid entry from the user, keep asking for the correct choice'
            while choice != '1' and choice != '2' and choice != 'quit':
                print("Invalid choice. Please try again.")
                user_options()
                choice = input()

            # choice is 1 or 2, so ask user for login credentials and url
            if choice != 'quit':
                           
                # format the correct url with subdomain
                url = 'https://' + subdomain + '.zendesk.com'
                          

                # For displaying summary of all tickets, get the ticket count first
                if choice == '1':
                    endpoint = url + '/api/v2/tickets/count'
                   
                # For displaying details of a single ticket get the ticket id
                else:
                    ticket_id = input("Enter ticket id: ")
                    endpoint = url + '/api/v2/tickets/' + ticket_id + '.json'
               

                try:  
                    response = requests.get(endpoint, auth = (user, password), timeout=3)
                    response.raise_for_status()

                except requests.exceptions.HTTPError as errh:
                    print ("Http Error:",errh)
                    exit(1)

                except requests.exceptions.ConnectionError as errc:
                    print ("Error Connecting to API:",errc)
                    exit(1)

                except requests.exceptions.Timeout as errt:
                    print ("Timeout Error:",errt)
                    exit(1)

                except requests.exceptions.RequestException as err:
                    print ("OOps: Something Else",err)
                    exit(1)
 
                  
                result = response.json()


                # Call the approprite function depending on the choice 
                if choice == '1':
                    total_tickets = result['count']['value']
                    get_all_tickets(url, user, password, total_tickets)
                   
                else:
                    get_single_ticket(result, ticket_id) 


            # user typed 'quit' after seeing options, so exit program
            else:
                print("Thanks for using the ticket viewer! Bye!!")
                exit(0)

    # quit will end the program
    else:
        print("Thanks for using Zendesk Ticket Viewer! ")
        exit(0)

if __name__ == '__main__':
    main()
