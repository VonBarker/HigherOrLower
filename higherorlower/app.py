import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QImage, QPixmap

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
        self.highscore = 0
        highscore_dict = {"highscore": self.highscore}
        
        try:
            with open('highscore.json', 'r', encoding='utf-8') as f:
                highscore_dict = json.load(f)
                self.highscore = highscore_dict["highscore"]
            print(self.highscore)
        except:
            with open('highscore.json', 'w', encoding='utf-8') as f:
                json.dump(highscore_dict, f, ensure_ascii=False, indent=4)

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
            self.cards_remaining = data["remaining"]
            print("Cards Remaining: " + str(self.cards_remaining))

            self.previous_card_value = self.card_value
        else:
            print("There was an error: {response.status_code}")

        #Card Image
        self.url_image = QImage()
        self.url_image.loadFromData(re.get(self.card_image).content)

        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(self.url_image))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.image_label)

        #Card suit and value
        self.card_info_label = QLabel(str(self.card_value) + " of " + self.card_suit)
        font = self.card_info_label.font()
        font.setPointSize(16)
        self.card_info_label.setFont(font)
        if (self.card_suit == "HEARTS" or self.card_suit == "DIAMONDS"): self.card_info_label.setStyleSheet("color: Red")
        else: self.card_info_label.setStyleSheet("color: Black")
        self.card_info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.card_info_label)

        #Score
        self.highscore_label = QLabel("Highscore: " + str(self.highscore))
        font = self.highscore_label.font()
        font.setPointSize(16)
        self.highscore_label.setFont(font)
        self.highscore_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.highscore_label)

        #Score
        self.score_label = QLabel("Score: " + str(self.points))
        font = self.score_label.font()
        font.setPointSize(16)
        self.score_label.setFont(font)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.score_label)

        #Higher or Lower Butttons
        def choose_higher():
            self.previous_card_value = self.card_value
            
            if self.cards_remaining > 0:
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
                    self.cards_remaining = data["remaining"]
                    print("Cards Remaining: " + str(self.cards_remaining))

                    self.url_image.loadFromData(re.get(self.card_image).content)
                    self.image_label.setPixmap(QPixmap(self.url_image))
                    self.card_info_label.setText(str(self.card_value) + " of " + self.card_suit)
                    if (self.card_suit == "HEARTS" or self.card_suit == "DIAMONDS"): self.card_info_label.setStyleSheet("color: Red")
                    else: self.card_info_label.setStyleSheet("color: Black")
                    self.cards_remaining_label.setText("Cards Remaining: " + str(self.cards_remaining))

                if int(self.card_value) > int(self.previous_card_value):
                    print("Correct")
                    self.points += 1
                    self.score_label.setText("Score: " + str(self.points))

                elif int(self.card_value) == int(self.previous_card_value):
                    print("They are the same.")
                    self.points += 1
                    self.score_label.setText("Score: " + str(self.points))
                else:
                    print("incorrect")
            
            if self.points > self.highscore:
                self.highscore = self.points
                self.highscore_label.setText("Highscore: " + str(self.highscore))
                highscore_dict = {"highscore": self.highscore}
                with open('highscore.json', 'w', encoding='utf-8') as f:
                    json.dump(highscore_dict, f, ensure_ascii=False, indent=4)


        def choose_lower():
            self.previous_card_value = self.card_value
            
            if self.cards_remaining > 0:
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
                    self.cards_remaining = data["remaining"]
                    print("Cards Remaining: " + str(self.cards_remaining))

                    self.url_image.loadFromData(re.get(self.card_image).content)
                    self.image_label.setPixmap(QPixmap(self.url_image))
                    self.card_info_label.setText(str(self.card_value) + " of " + self.card_suit)
                    if (self.card_suit == "HEARTS" or self.card_suit == "DIAMONDS"): self.card_info_label.setStyleSheet("color: Red")
                    else: self.card_info_label.setStyleSheet("color: Black")
                    self.cards_remaining_label.setText("Cards Remaining: " + str(self.cards_remaining))

                if int(self.card_value) < int(self.previous_card_value):
                    print("Correct")
                    self.points += 1
                    self.score_label.setText("Score: " + str(self.points))

                elif int(self.card_value) == int(self.previous_card_value):
                    print("They are the same.")
                    self.points += 1
                    self.score_label.setText("Score: " + str(self.points))
                else:
                    print("incorrect")

            if self.points > self.highscore:
                self.highscore = self.points
                self.highscore_label.setText("Highscore: " + str(self.highscore))
                highscore_dict = {"highscore": self.highscore}
                with open('highscore.json', 'w', encoding='utf-8') as f:
                    json.dump(highscore_dict, f, ensure_ascii=False, indent=4)

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
        lower_button.clicked.connect(choose_lower)

        layout.addLayout(button_layout)

        #Cards Remaining
        self.cards_remaining_label = QLabel("Cards Remaining: " + str(self.cards_remaining))
        font = self.cards_remaining_label.font()
        font.setPointSize(16)
        self.cards_remaining_label.setFont(font)
        layout.addWidget(self.cards_remaining_label)

        widgets = QWidget()
        widgets.setLayout(layout)
        self.setCentralWidget(widgets)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()