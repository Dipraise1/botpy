import requests
import json  # Import the json module for serialization

# Telegram Bot API endpoint
BASE_URL = "https://api.telegram.org/bot6954064524:AAHHNIOHMi3AFRTZBriOIRUBei8kdgJYQ7E/"

user_data = {}

# Function to send a message using the Telegram Bot API
def send_message(chat_id, text, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup,
    }
    response = requests.post(BASE_URL + 'sendMessage', json=payload)
    return response.json()

# Function to send role options
def send_role_options(chat_id):
    options = {
        'keyboard': [['Software Developer', 'Graphic Designer'], ['Web Developer', 'Marketer'], ['Raider', 'Blockchain Engineer'], ['Software Tester'], ['Done']],
        'resize_keyboard': True,
        'one_time_keyboard': True,
    }
    send_message(chat_id, 'Select your role:', json.dumps(options))

# Function to prompt for charge input
def send_charge_prompt(chat_id, role):
    send_message(chat_id, f'Enter the amount you would charge for {role}:')

# Handler for incoming messages
def handle_message(update):
    message = update['message']
    chat_id = message['chat']['id']
    text = message.get('text', '')

    global user_data  # Declare user_data as global

    if chat_id not in user_data:
        user_data[chat_id] = {'roles': []}

    if text.lower() == '/start':
        # Send a welcome message and options
        options = {
            'keyboard': [['Initialize a trade', 'Apply as a web3 freelancer']],
            'resize_keyboard': True,
            'one_time_keyboard': True,
        }
        send_message(chat_id, 'Hey! Welcome. What do you want to do today?', json.dumps(options))
    elif text.lower() == 'initialize a trade':
        send_service_options(chat_id)
    elif text.lower() == 'apply as a web3 freelancer':
        user_data[chat_id]['hiring'] = False
        send_role_options(chat_id)
    elif text.lower() in ['software developer', 'graphic designer', 'web developer', 'marketer', 'raider', 'blockchain engineer', 'software tester']:
        role = text.lower()
        user_data[chat_id]['roles'].append(role)
        send_charge_prompt(chat_id, role)
    elif text.lower() == 'done':
        send_message(chat_id, 'Thank you for providing the information!')
    elif text.lower() == 'back':
        send_message(chat_id, 'What do you want to do today?', json.dumps({'keyboard': [['Initialize a trade', 'Apply as a web3 freelancer']], 'resize_keyboard': True, 'one_time_keyboard': True}))
    elif 'hiring' in user_data[chat_id] and text.lower().startswith('$'):
        user_data[chat_id]['price_list'] = text
        send_message(chat_id, 'Your price has been recorded successfully!')

# Function to send service options
def send_service_options(chat_id):
    options = {
        'keyboard': [['software developer', 'graphic designer', 'web developer', 'marketer', 'raider', 'blockchain engineer', 'software tester'], ['Back']],
        'one_time_keyboard': True,
    }
    send_message(chat_id, 'Select the service you want:', json.dumps(options))

# Main function to handle updates
def main():
    offset = None
    while True:
        response = requests.get(BASE_URL + 'getUpdates', params={'offset': offset})
        updates = response.json()['result']
        for update in updates:
            handle_message(update)
            offset = update['update_id'] + 1

if __name__ == "__main__":
    main()
