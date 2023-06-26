import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Initialize the Flask app
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = "your_secret_key"

# Initialize the socket instance
socketio = SocketIO(app)

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_identifier(self):
        return str(self)

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ['C', 'D', 'H', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        total = 0
        num_aces = 0

        for card in self.hand:
            if isinstance(card.rank, int):
                if card.rank > 10:
                    total += 10
            elif card.rank == "A":
                total += 11
                num_aces += 1
            elif isinstance(card.rank, int):
                total += card.rank
            elif isinstance(card.rank, str):
                if card.rank == "J":
                    total += 11
                elif card.rank == "Q":
                    total += 12
                elif card.rank == "K":
                    total += 13

        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1

        return total

    def __str__(self):
        return f"{self.name}'s hand: {', '.join(str(card) for card in self.hand)}"

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def start(self):
        self.deck.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        self.player1.add_card(self.deck.deal())
        self.player2.add_card(self.deck.deal())
        self.player1.add_card(self.deck.deal())
        self.player2.add_card(self.deck.deal())

    def hit(self, player):
        card = self.deck.deal()
        player.add_card(card)

    def end_game(self):
        player1_value = self.player1.get_hand_value()
        player2_value = self.player2.get_hand_value()

        if player1_value > 21 or (player2_value <= 21 and player2_value > player1_value):
            return "Player 2 wins!"
        elif player2_value > 21 or (player1_value <= 21 and player1_value > player2_value):
            return "Player 1 wins!"
        elif player1_value == player2_value:
            return "It's a tie!"
        else:
            return "Unknown result"

game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('deal_card')
def deal_card():
    card = deck.deal()
    emit('card_dealt', {'card': str(card)})

@app.route('/deal')
def deal():
    game.start()
    return "Game started. Cards dealt."

@app.route('/hit')
def hit():
    player = request.args.get('player')
    if player == '1':
        game.hit(game.player1)
    elif player == '2':
        game.hit(game.player2)
    return "Card dealt."

@app.route('/end')
def end():
    result = game.end_game()
    return result

if __name__ == '__main__':
    socketio.run(app)
