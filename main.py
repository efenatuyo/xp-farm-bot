import requests, time, random

DISCORD_TOKEN = ''
CHANNEL_ID = [1136563378559651930, 1136928147284181062]  # Replace with the ID of the channel you want to fetch messages from and send messages to

headers = {
    'Authorization': f'{DISCORD_TOKEN}'
}

class MessageManager:
    def __init__(self, max_messages=5000):
        self.max_messages = max_messages
        self.messages = []

    def add_messages(self, new_messages):
        unique_new_messages = [msg for msg in new_messages if msg not in self.messages]
        self.messages.extend(unique_new_messages)
        if len(self.messages) > self.max_messages:
            num_messages_to_remove = len(self.messages) - self.max_messages
            self.messages = self.messages[num_messages_to_remove:]

    def get_messages(self):
        return self.messages
 
message_manager = MessageManager(max_messages=1000)
def react_to_message(channel_id, message_id, emoji):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    headers = {
        "Authorization": f"{DISCORD_TOKEN}"
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 204:
        print("Reacted to the message!")
    else:
        print(f"Failed to react to the message. Status code: {response.status_code}, Error: {response.text}")

def send_discord_message(channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
    'Authorization': f'{DISCORD_TOKEN}'
}
    payload = {
        "content": message
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"send {message}, {channel_id}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Error: {response.text}")
        
def fetch_channel_messages(channel_id, limit):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    params = {
        'limit': min(limit, 100)
    }
    messages = []

    while len(messages) < limit:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        new_messages = response.json()
        if not new_messages:
            break
        messages.extend(new_messages)
        params['before'] = new_messages[-1]['id']

    return messages

def main():
 messages = fetch_channel_messages(random.choice(CHANNEL_ID), 100)
 print(messages)
 message_content_list = [message['content'] for message in messages]
 message_manager.add_messages(message_content_list)
 numero = 0
 while True:
    if numero % 10 == 0:
       messages = fetch_channel_messages(random.choice(CHANNEL_ID), 100)
       message_content_list = [message['content'] for message in messages]
       message_manager.add_messages(message_content_list)
    a = random.choice(CHANNEL_ID)
    b = random.choice(message_manager.get_messages())
    if "discord.gg" in b: continue
    send_discord_message(a, b)
    numero += 1
    time.sleep(random.randint(1, 20))
        

while True:
  try:
    main()
  except Exception as e: 
    print(e)
    continue
