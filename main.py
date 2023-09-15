import openai

openai.api_key = 'YOUR_API_KEY'

# System message to be sent to the model
system_message = "you are a trello agent. I will give you a query and you'll have to decide appropriate cli command for doing that task. Im giving you a python script which you can see to make appropriate cli command. Just give me the command, nothing else. Python code-\nimport argparse\nimport requests\n\n# Replace 'YOUR_API_KEY' and 'YOUR_TOKEN' with your actual Trello credentials\nAPI_KEY = 'YOUR_API_KEY'\nTOKEN = 'YOUR_TOKEN'\n\ndef create_card(board_id, list_id, name, description=''):\n    url = f'https://api.trello.com/1/cards?key={API_KEY}&token={TOKEN}&idBoard={board_id}&idList={list_id}&name={name}&desc={description}'\n    response = requests.post(url)\n    return response\n\ndef create_list(board_id, name):\n    url = f'https://api.trello.com/1/lists?key={API_KEY}&token={TOKEN}&idBoard={board_id}&name={name}'\n    response = requests.post(url)\n    return response\n\nif __name__ == \"__main__\":\n    parser = argparse.ArgumentParser(description=\"Trello CLI Tool\")\n    parser.add_argument(\"action\", choices=[\"create_card\", \"create_list\"], help=\"Action to perform\")\n    parser.add_argument(\"--board_id\", help=\"Trello board ID\")\n    parser.add_argument(\"--list_id\", help=\"Trello list ID\")\n    parser.add_argument(\"--name\", help=\"Name for the card or list\")\n    parser.add_argument(\"--description\", help=\"Description for the card\")\n\n    args = parser.parse_args()\n\n    if args.action == \"create_card\":\n        if not args.board_id or not args.list_id or not args.name:\n            print(\"Error: board_id, list_id, and name are required for creating a card.\")\n        else:\n            response = create_card(args.board_id, args.list_id, args.name, args.description)\n            print(response.text)\n\n    elif args.action == \"create_list\":\n        if not args.board_id or not args.name:\n            print(\"Error: board_id and name are required for creating a list.\")\n        else:\n            response = create_list(args.board_id, args.name)\n            print(response.text)\n"

def get_response(user_query):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message['content']

if __name__ == "__main__":
    while True:
        user_query = input("Enter your query: ")
        print(get_response(user_query))
