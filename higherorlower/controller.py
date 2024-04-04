import requests as re
import json

from PIL import Image
import requests
from io import BytesIO

response = requests.get(https://deckofcardsapi.com/static/img/5S.png)
img = Image.open(BytesIO(response.content))

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

response = re.get(url)

if response.ok:
    print(response.text)
    data = json.loads(response.text)
    deck_id = data["deck_id"]
    print(deck_id)
else:
    print("There was an error: {response.status_code}")

base_url = "https://deckofcardsapi.com/api/deck/"

draw_card_url = draw_card_url = "/draw/?count=1"

url = base_url + deck_id + draw_card_url

response = re.get(url)

if response.ok:
    print(response.text)
    data = json.loads(response.text)
    card_value = data["cards"][0]["value"]
    if card_value == "ACE": card_value = 14
    elif card_value == "KING": card_value = 13
    elif card_value == "QUEEN": card_value = 12
    elif card_value == "JACK": card_value = 11
    print(card_value)
    card_image = data["cards"][0]["images"]["png"]
else:
    print("There was an error: {response.status_code}")