import requests
import math
import getpass


def get_user_cred():
    user = input("\nPlease enter your email address for your Zendesk account: ")
    password = getpass.getpass("Please enter your password for your Zendesk account: ")
    subdomain = input("Please enter your Zendesk subdomain e.g. zccfistlast: ")
 
    print('Thanks for providing your credentials. Now you will be asked about your option...')
    return subdomain, user, password


# print the different options text to output
def user_options():
    print("\nSelect from the available options below: ")
    print(" - Press 1 to view All Tickets")
    print(" - Press 2 to view a Single Ticket")
    print(" - Type 'quit' to exit")



# returns all tickets for a page
def call_zendesk_api(url, user, password):
    response = requests.get(url, auth = (user, password))
    return response.json()


def list_tickets(current_list, current_page_number, last_page_number):
    if current_page_number != 1:
        print('. . .')
    for tickets in current_list['tickets']:
        # Formatting Subject lines and Ticket numbers to have same length
        summary = (tickets['subject']).ljust(35)[:35]
        ticket_number = str(tickets['id']).ljust(5)[:5]
        print(ticket_number + ' ' + '  Subject: ' + summary + '   ' + '   Status: ' + tickets['status'] + '    Last updated:' + tickets['updated_at'])
    if current_page_number < last_page_number:
        print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - -  ')
        print('- - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - -  ')




# A ticket viewer program for Zendesk accounts (Get all or Get single)
def main():
    print("--------------------------------")
    print("Welcome to Zendesk Ticket Viewer")
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
                           
                # format the url with subdomain
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
                    print ("Error Connecting:",errc)
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
                print("Thanks for using the ticket viewer. Goodbye.")
                exit(0)

    # quit will end the program
    else:
        print("Thanks for using Zendesk Ticket Viewer! ")
        exit(0)

if __name__ == '__main__':
    main()
