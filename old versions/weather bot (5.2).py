import requests
from config import token
import time

base_url = 'https://api.telegram.org/bot'
# chat_id = '487455457'


chat_id = '211198621'
text = 'Хрю-хрю-хрю!'

while True:
    response = requests.get(base_url + token + '/sendMessage',
                        params={
                                'chat_id': chat_id,
                                'text': text
                        }
)
    print(response.json())
# print(response.url)
# Code executed here
    time.sleep(1)
    