import requests, time, random

mesga = ["yo", "!", "?", "pff", "rah", "cool", "wow", "nice", "okay", "bye", "lol", "oops", "ouch", "thanks", "yes", "no", "brb", "omg", "haha", "uh-oh", "hmm", "wut", "sure", "ok", "oh", "meh", "yeah", "alright", "got it", "yikes", "whoa", "right", "well", "later", "gotcha", "nope", "yay", "nice try", "wait", "what?", "sorry", "please", "perfect", "congrats", "woohoo", "amazing", "go", "how", "good", "take care", "bravo", "pro", "bingo", "awesome", "wow!", "thanks!", "excellent", "what?!", "dope", "lit", "fire", "sick", "chill", "bruh", "lit af", "on fleek", "savage", "yas", "let's go", "shook", "AF", "gimme", "suh", "salty", "bop", "dank", "bae", "woke", "yolo", "finesse", "gig", "skrrt", "fleek", "wavy", "trendy", "litty", "rad", "fuego", "boss", "heya", "hype", "we out here", "flexin'", "swoll", "thicc", "bet", "finna", "lowkey", "highkey", "glo-up", "yasss", "yeet", "ghost", "lituation", "gucci", "snatched", "yeehaw", "bougie", "beast mode", "mood", "vibey", "turnt up", "salty af", "drippin'", "slay", "stan", "woke af", "turnt", "shooketh", "betty", "ship", "kiki", "swerve", "totes adorbs", "yas queen", "can't even", "fleeky", "throwing shade", "yeet", "goals", "mood", "yeehaw", "bougie", "savage mode", "swaggy", "beast mode", "squad up", "flexin' on 'em", "drippin' swag", "stay slayin'", "vibey", "turnt up", "chillin' like a villain", "fam squad", "all the feels", "so fetch", "killin' it", "bougie", "savage mode", "swaggy", "beast mode", "blessed and highly favored", "mood", "lit city", "vibey", "turnt up", "chillin' like a villain", "flexin' on 'em", "dripp"]


DISCORD_TOKEN = ''
CHANNEL_ID = [1136928147284181062, 1136995488005095525]  # Replace with the ID of the channel you want to fetch messages from
MESSAGE_LIMIT = 100

headers = {
    'Authorization': f'{DISCORD_TOKEN}'
}

def save_messages_to_file(messages, file_path = "messages.txt"):
    with open(file_path, 'w', encoding='utf-8') as file:
        for message in messages:
            file.write(message + '\n')
            
def load_messages_from_file(file_path = "messages.txt"):
    with open(file_path, 'r', encoding='utf-8') as file:
        messages = [line.strip() for line in file]

    return messages

class MessageManager:
    def __init__(self, max_messages=float("inf")):
        self.max_messages = max_messages
        self.messages = load_messages_from_file()

    def add_messages(self, new_messages):
        unique_new_messages = [msg for msg in new_messages if msg not in self.messages]
        self.messages.extend(unique_new_messages)

        if len(self.messages) > self.max_messages:
            num_messages_to_remove = len(self.messages) - self.max_messages
            self.messages = self.messages[num_messages_to_remove:]
            save_messages_to_file(self.messages)

    def get_messages(self):
        return self.messages
 
message_manager = MessageManager()
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
        if random.randint(1, 2) == 1:
            react_to_message(channel_id, response.json().get('id'), "💀")
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
 messages = fetch_channel_messages(random.choice(CHANNEL_ID), MESSAGE_LIMIT)
 print(messages)
 message_content_list = [message['content'] for message in messages]
 message_manager.add_messages(message_content_list)
 numero = 0
 while True:
    if numero % 10 == 0:
       messages = fetch_channel_messages(random.choice(CHANNEL_ID), MESSAGE_LIMIT)
       message_content_list = [message['content'] for message in messages]
       message_manager.add_messages(message_content_list)
    a = random.choice(CHANNEL_ID)
    b = random.choice(message_manager.get_messages()) + " " + random.choice(mesga)
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
