import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = range(1, 14)

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
            if card.rank > 10:
                total += 10
            elif card.rank == 1:
                total += 11
                num_aces += 1
            else:
                total += card.rank

        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1

        return total

    def __str__(self):
        return f"{self.name}'s hand: {', '.join(str(card) for card in self.hand)}"

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def start(self):
        print("Welcome to Blackjack!")
        self.deck.shuffle()
        self.deal_initial_cards()

        while True:
            print(self.player)
            print(f"Dealer's hand: {self.dealer.hand[0]}")

            choice = input("Do you want to hit or stand? (h/s): ").lower()

            if choice == 'h':
                self.hit()
                if self.player.get_hand_value() > 21:
                    self.end_game()
                    break
            elif choice == 's':
                self.stand()
                break
            else:
                print("Invalid choice. Please try again.")

    def deal_initial_cards(self):
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def hit(self):
        card = self.deck.deal()
        self.player.add_card(card)
        print(f"You drew: {card}")

    def stand(self):
        while self.dealer.get_hand_value() < 17:
            card = self.deck.deal()
            self.dealer.add_card(card)
            print(f"Dealer drew: {card}")

        self.end_game()

    def end_game(self):
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        print("Final hands:")
        print(self.player)
        print(self.dealer)

        if player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
            print("Dealer wins!")
        elif player_value == dealer_value:
            print("It's a tie!")
        else:
            print("Player wins!")

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'y':
            self.reset()
            self.start()
        else:
            print("Thank you for playing!")

    def reset(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

