class Player(object):
    def __init__(self, name, hand=None):
        self.name = name
        self.hands = [hand]
        self.money = 1000

    def set_hand(self, new_hand):
        self.hands = [new_hand]

    def hit(self, hand, shoe):
        c = shoe.deal()
        hand.add_card(c)

    def split(self, hand):
        self.hands.append(hand.split())
        self.money -= hand.bet

    def bet(self, hand, amount):
        if self.money > amount:
            hand.add_bet(amount)
            self.money -= amount
        else:
            raise ValueError("Player can not bet more than he has")

    def double_down(self, hand, shoe):
        if self.money > hand.bet:
            self.money -= hand.bet
            hand.add_bet(hand.bet)
            self.hit(hand, shoe)
            hand.stay()
        else:
            raise ValueError("Player can not bet more than he has")

    def stay(self, hand):
        if not hand.stayed:
            hand.stay()
        else:
            raise ValueError("Cannot stay on stayed hand")
