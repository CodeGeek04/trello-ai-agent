import argparse
import requests
import random

# Replace 'YOUR_API_KEY' and 'YOUR_TOKEN' with your actual Trello credentials
API_KEY = 'YOUR_API_KEY'
TOKEN = 'YOUR_TOKEN'

def get_board_list(api_key, token):
    # Get a list of your Trello boards
    url = f'https://api.trello.com/1/members/me/boards?key={api_key}&token={token}'
    response = requests.get(url)
    boards = response.json()

    # Check if you have at least one board
    if not boards:
        return None, None

    # Select a random board from the list
    random_board = random.choice(boards)
    board_id = random_board['id']
    board_name = random_board['name']

    # Get the lists for the selected board
    url = f'https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={token}'
    response = requests.get(url)
    lists = response.json()

    if not lists:
        return board_name, None

    # Select a random list from the board
    random_list = random.choice(lists)
    list_id = random_list['id']
    list_name = random_list['name']

    return board_id, list_id

def create_card(board_id, list_id, name, description=''):
    board_id, list_id = get_board_list(API_KEY, TOKEN)
    while list_id is None:
        board_id, list_id = get_board_list(API_KEY, TOKEN)

    url = f'https://api.trello.com/1/cards?key={API_KEY}&token={TOKEN}&idBoard={board_id}&idList={list_id}&name={name}&desc={description}'
    response = requests.post(url)
    return response

def create_list(board_id, name):
    board_id, list_id = get_board_list(API_KEY, TOKEN)
    url = f'https://api.trello.com/1/lists?key={API_KEY}&token={TOKEN}&idBoard={board_id}&name={name}'
    response = requests.post(url)
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trello CLI Tool")
    parser.add_argument("action", choices=["create_card", "create_list"], help="Action to perform")
    parser.add_argument("--board_id", help="Trello board ID")
    parser.add_argument("--list_id", help="Trello list ID")
    parser.add_argument("--name", help="Name for the card or list")
    parser.add_argument("--description", help="Description for the card")

    args = parser.parse_args()

    if args.action == "create_card":
        if not args.board_id or not args.list_id or not args.name:
            print("Error: board_id, list_id, and name are required for creating a card.")
        else:
            response = create_card(args.board_id, args.list_id, args.name, args.description)
            print(response.text)

    elif args.action == "create_list":
        if not args.board_id or not args.name:
            print("Error: board_id and name are required for creating a list.")
        else:
            response = create_list(args.board_id, args.name)
            print(response.text)
