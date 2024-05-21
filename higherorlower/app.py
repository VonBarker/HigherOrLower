import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt

import requests as re
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        #Title
        self.setWindowTitle("Higher or Lower Game")
        title = QLabel("Higher or Lower Game")
        font = title.font()
        font.setPointSize(24)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(title)

        self.setFixedSize(QSize(400, 600))

        #Function
        self.points = 0

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
            self.card_value = data["cards"][0]["value"]
            self.card_suit = data["cards"][0]["suit"]
            if self.card_value == "ACE": self.card_value = 14
            elif self.card_value == "KING": self.card_value = 13
            elif self.card_value == "QUEEN": self.card_value = 12
            elif self.card_value == "JACK": self.card_value = 11
            self.card_image = data["cards"][0]["images"]["png"]
            cards_remaining = data["remaining"]
            print("Cards Remaining: " + str(cards_remaining))

            self.previous_card_value = self.card_value
        else:
            print("There was an error: {response.status_code}")

        #Card Image Here

        #Card suit and value
        card_info_label = QLabel(str(self.card_value) + " of " + self.card_suit)
        font = card_info_label.font()
        font.setPointSize(16)
        card_info_label.setFont(font)
        if (self.card_suit == "HEARTS" or self.card_suit == "DIAMONDS"): card_info_label.setStyleSheet("color: Red")
        else: card_info_label.setStyleSheet("color: Black")
        card_info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(card_info_label)

        #Score
        score_label = QLabel("Score: " + str(self.points))
        font = score_label.font()
        font.setPointSize(16)
        score_label.setFont(font)
        score_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(score_label)

        #Higher or Lower Butttons
        def choose_higher():
            if int(self.card_value) > int(self.previous_card_value):
                print("Correct")
                self.points += 1

            elif int(self.card_value) == int(self.previous_card_value):
                print("They are the same.")
                self.points += 1
            else:
                print("incorrect")

            self.previous_card_value = self.card_value

            response = re.get(url)

            if response.ok:
                data = json.loads(response.text)
                self.card_value = data["cards"][0]["value"]
                self.card_suit = data["cards"][0]["suit"]
                if self.card_value == "ACE": self.card_value = 14
                elif self.card_value == "KING": self.card_value = 13
                elif self.card_value == "QUEEN": self.card_value = 12
                elif self.card_value == "JACK": self.card_value = 11
                self.card_image = data["cards"][0]["images"]["png"]
                cards_remaining = data["remaining"]
                print("Cards Remaining: " + str(cards_remaining))

        button_layout = QHBoxLayout()

        higher_button = QPushButton("Higher")
        font = higher_button.font()
        font.setPointSize(16)
        higher_button.setFont(font)
        higher_button.setStyleSheet("color: Green")
        button_layout.addWidget(higher_button)
        higher_button.clicked.connect(choose_higher)

        lower_button = QPushButton("Lower")
        font = lower_button.font()
        font.setPointSize(16)
        lower_button.setFont(font)
        lower_button.setStyleSheet("color: Red")
        button_layout.addWidget(lower_button)
        lower_button.clicked.connect(choose_higher)

        layout.addLayout(button_layout)


        widgets = QWidget()
        widgets.setLayout(layout)
        self.setCentralWidget(widgets)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()