class Hand(object):
    _value = 0
    _aces = []
    _aces_soft = 0
    split_hand = False
    stayed = False

    def __init__(self, cards, bet=None):
        self.cards = cards
        self.bet = bet

    def __str__(self):
        return ', '.join(str(c) for c in self.cards) + ' -> ' + str(self.value)

    @property
    def value(self):
        self._value = 0
        for c in self.cards:
            self._value += c.value

        if self._value > 21 and self.aces_soft > 0:
            for ace in self.aces:
                if ace.value == 11:
                    self._value -= 10
                    ace.value = 1
                    if self._value <= 21:
                        break
        return self._value

    @property
    def aces(self):
        self._aces = []
        for c in self.cards:
            if c.rank == "Ace":
                self._aces.append(c)
        return self._aces

    @property
    def aces_soft(self):
        self._aces_soft = 0
        for ace in self.aces:
            if ace.value == 11:
                self._aces_soft += 1
        return self._aces_soft

    def splitable(self):
        return self.length() == 2 and self.cards[0].value == self.cards[1].value

    def blackjack(self):
        return not self.split_hand and self.value == 21 and self.length() == 2

    def busted(self):
        return self.value > 21

    def stay(self):
        self.stayed = True

    def add_card(self, card):
        self.cards.append(card)

    def split(self):
        self.split_hand = True
        c = self.cards.pop()
        new_hand = Hand([c], self.bet)
        new_hand.split_hand = True
        return new_hand

    def length(self):
        return len(self.cards)

    def add_bet(self, bet):
        self.bet += bet
