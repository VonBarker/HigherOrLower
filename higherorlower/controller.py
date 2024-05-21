import requests as re
import json

from PyQt6.QtGui import QPixmap, QIcon
import urllib
from PyQt6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        label = QLabel(self) 
        url = 'https://deckofcardsapi.com/static/img/6H.png'    
        data = urllib.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

points = 0

game_intro = "This is a game of higher or lower. "
game_intro += "A card will be drawn and then you must guess if the next card will be higher or lower. "
game_intro += "Since this game uses a deck of cards you can make your guesses based on the cards you have already pulled."
game_intro += "\n\nHit enter to start the game.\n"

input(game_intro)

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

response = re.get(url)

if response.ok:
    data = json.loads(response.text)
    deck_id = data["deck_id"]
    print(deck_id + "\n")
else:
    print("There was an error: {response.status_code}")

base_url = "https://deckofcardsapi.com/api/deck/"

draw_card_url = "/draw/?count=1"

url = base_url + deck_id + draw_card_url

response = re.get(url)

if response.ok:
    data = json.loads(response.text)
    card_value = data["cards"][0]["value"]
    card_suit = data["cards"][0]["suit"]
    print("\n" + str(card_value) + " of " + card_suit)
    if card_value == "ACE": card_value = 14
    elif card_value == "KING": card_value = 13
    elif card_value == "QUEEN": card_value = 12
    elif card_value == "JACK": card_value = 11
    card_image = data["cards"][0]["images"]["png"]
    cards_remaining = data["remaining"]
    print("Cards Remaining: " + str(cards_remaining))

    user_input = input("1. Higher\n2. Lower\n")
else:
    print("There was an error: {response.status_code}")

while cards_remaining > 0:
    previous_card_value = card_value

    response = re.get(url)

    if response.ok:
        data = json.loads(response.text)
        card_value = data["cards"][0]["value"]
        card_suit = data["cards"][0]["suit"]
        print("\n" + str(card_value) + " of " + card_suit)
        if card_value == "ACE": card_value = 14
        elif card_value == "KING": card_value = 13
        elif card_value == "QUEEN": card_value = 12
        elif card_value == "JACK": card_value = 11
        card_image = data["cards"][0]["images"]["png"]
        cards_remaining = data["remaining"]
        print("Cards Remaining: " + str(cards_remaining) + "\n")

        if user_input == "1" and int(card_value) > int(previous_card_value):
            print("Correct")
            points += 1
        elif user_input == "2" and int(card_value) < int(previous_card_value):
            print("Correct")
            points += 1
        elif int(card_value) == int(previous_card_value):
            print("They are the same.")
            points += 1
        elif user_input == "3":
            break
        else:
            print("incorrect")
        user_input = input("1. Higher\n2. Lower\n3. Finish Early\n")
    else:
        print("There was an error: {response.status_code}")

print("You Scored: " + str(points) + " points")