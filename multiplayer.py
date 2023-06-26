import random
import tkinter as tk
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Game state
game_state = {
    'players': {},
    'turn': None,
    'game_over': False,
    'deck': None
}

class BlackjackGUI:
    def __init__(self, root, player_id):
        self.root = root
        self.player_id = player_id
        self.deck = None
        self.player = Player(player_id)
        self.dealer = Player("Dealer")

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="green")
        self.canvas.pack()

        self.card_images = {}  # Dictionary to store card images

        # Load card images
        suits = ['C', 'D', 'H', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                card_name = card.get_identifier()
                card_image = ImageTk.PhotoImage(Image.open(f'cards/{rank}{suit}.png'))
                self.card_images[str(card_name)] = card_image

        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Welcome to Blackjack!", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.player_label = tk.Label(self.root, text="Player's hand:", font=("Arial", 12))
        self.player_label.pack()

        self.player_hand_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.player_hand_label.pack()

        self.dealer_label = tk.Label(self.root, text="Dealer's hand:", font=("Arial", 12))
        self.dealer_label.pack()

        self.dealer_hand_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.dealer_hand_label.pack()

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.hit_button = tk.Button(self.root, text="Hit", width=10, command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.root, text="Stand", width=10, command=self.stand)
        self.stand_button.pack(side=tk.LEFT)

    def start_game(self):
        self.deck = game_state['deck']
        self.deal_initial_cards()
        self.update_hands()

    def deal_initial_cards(self):
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def hit(self):
        card = self.deck.deal()
        self.player.add_card(card)
        self.update_hands()

        if self.player.get_hand_value() > 21:
            self.end_game("Dealer wins!")

    def stand(self):
        while self.dealer.get_hand_value() < 17:
            card = self.deck.deal()
            self.dealer.add_card(card)
            self.update_hands()

        self.end_game()

    def end_game(self, message=None):
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        self.result_label.config(text="Final hands:\n" + str(self.player) + "\n" + str(self.dealer))

        if player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
            if message is None:
                message = "Dealer wins!"
        elif player_value == dealer_value:
            message = "It's a tie!"
        else:
            message = "Player wins!"

        play_again = messagebox.askyesno("Game Over", message + "\nDo you want to play again?")
        if play_again:
            self.reset()
            self.start_game()
        else:
            self.root.destroy()

    def reset(self):
        self.player = Player(self.player_id)
        self.dealer = Player("Dealer")

    def update_hands(self):
        self.canvas.delete("all")  # Clear the canvas

        player_hand = self.player.hand
        dealer_hand = self.dealer.hand

        # Draw player's hand
        for i, card in enumerate(player_hand):
            x = 100 + i * 100
            y = 300
            self.draw_card(x, y, card)

        # Draw dealer's hand (show only one card)
        self.draw_card(100, 100, dealer_hand[0])

        self.player_hand_label.config(text=str(self.player))
        self.dealer_hand_label.config(text=str(self.dealer))

        # Emit updated hands to other players
        emit('update_hands', {'player_id': self.player_id, 'player_hand': str(self.player), 'dealer_hand': str(self.dealer)})

    def draw_card(self, x, y, card):
        card_identifier = card.get_identifier()

        if card_identifier in self.card_images:
            card_image = self.card_images[card_identifier]

            if not hasattr(card_image, "animated"):
                card_image.animated = True

                # Calculate the x-coordinate dynamically based on the number of cards and the canvas width
                canvas_width = self.canvas.winfo_width()
                card_width = card_image.width()
                num_cards = len(self.player.hand)
                total_width = num_cards * card_width
                padding = (canvas_width - total_width) // 2
                x = padding + (num_cards - 1) * card_width // 2

                # Create the card image on the canvas
                card_id = self.canvas.create_image(x, y, image=card_image, anchor=tk.CENTER)

                # Animation effect: gradually move the card from top to the specified position
                initial_y = y - 200  # Initial y-coordinate above the canvas
                step = 10  # Move 10 pixels at a time
                delay = 20  # Delay between each movement (milliseconds)

                def animate():
                    nonlocal y
                    if y > initial_y:
                        self.canvas.move(card_id, 0, -step)
                        y -= step
                        self.canvas.after(delay, animate)

                animate()
            else:
                card_id = self.canvas.create_image(x, y, image=card_image, anchor=tk.CENTER)
        else:
            print(f"Card image not found for card: {card}")


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
        self.players = {}
        self.dealer = Player("Dealer")

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)

    def start(self):
        self.deck.shuffle()
        self.deal_initial_cards()

    def deal_initial_cards(self):
        for player in self.players.values():
            player.add_card(self.deck.deal())
            player.add_card(self.deck.deal())

        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def hit(self, player_id):
        player = self.players.get(player_id)
        if player:
            card = self.deck.deal()
            player.add_card(card)
            return str(card)
        return None

    def stand(self, player_id):
        player = self.players.get(player_id)
        if player:
            while self.dealer.get_hand_value() < 17:
                card = self.deck.deal()
                self.dealer.add_card(card)
            return str(self.dealer)
        return None

    def get_player_hand(self, player_id):
        player = self.players.get(player_id)
        if player:
            return str(player)
        return None

    def get_dealer_hand(self):
        return str(self.dealer)

    def get_game_result(self, player_id):
        player = self.players.get(player_id)
        if player:
            player_value = player.get_hand_value()
            dealer_value = self.dealer.get_hand_value()

            if player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
                return "Dealer wins!"
            elif player_value == dealer_value:
                return "It's a tie!"
            else:
                return "Player wins!"
        return None

    def reset(self):
        self.deck = Deck()
        self.players = {}
        self.dealer = Player("Dealer")


game = Game()

@app.route('/')
def index():
    return "Blackjack Multiplayer Game"

@socketio.on('connect')
def handle_connect():
    player_id = request.sid
    game.add_player(player_id)
    emit('player_connected', {'player_id': player_id})

@socketio.on('start_game')
def handle_start_game():
    game.start()
    deck = game.deck
    game_state['deck'] = deck
    emit('game_started')

@socketio.on('hit')
def handle_hit():
    player_id = request.sid
    card = game.hit(player_id)
    emit('card_dealt', {'card': card}, broadcast=True)

@socketio.on('stand')
def handle_stand():
    player_id = request.sid
    dealer_hand = game.stand(player_id)
    emit('dealer_hand', {'dealer_hand': dealer_hand}, broadcast=True)

@socketio.on('get_hands')
def handle_get_hands():
    player_id = request.sid
    player_hand = game.get_player_hand(player_id)
    dealer_hand = game.get_dealer_hand()
    emit('update_hands', {'player_id': player_id, 'player_hand': player_hand, 'dealer_hand': dealer_hand})

@socketio.on('get_result')
def handle_get_result():
    player_id = request.sid
    result = game.get_game_result(player_id)
    emit('game_result', {'result': result})

@socketio.on('reset_game')
def handle_reset_game():
    game.reset()
    emit('game_reset')

if __name__ == '__main__':
    socketio.run(app, debug=True)
