from random import shuffle
from Card import Card
from Constants import RANKS, SUITS, DECK_SIZE, SHOE_USAGE_BEFORE_RESHUFFLE


class Shoe(object):
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = self.shuffled_cards()

    def __str__(self):
        s = ""
        for c in self.cards:
            s += "%s\n" % c
        return s

    def shuffled_cards(self):
        cards = []
        for deck in range(self.num_decks):
            for rank in RANKS:
                for suit in SUITS:
                    cards.append(Card(rank, suit))
        shuffle(cards)
        return cards

    def deal(self):
        if self.shoe_usage() < SHOE_USAGE_BEFORE_RESHUFFLE:
            self.cards = self.shuffled_cards()
        card = self.cards.pop()
        return card

    def shoe_usage(self):
        return len(self.cards) / (DECK_SIZE * self.num_decks)
