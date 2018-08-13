import sys

from Constants import DECKS_IN_SHOE, MINIMUM_BET, WIN_MULTIPLIER, SPLIT_LIMIT
from Dealer import Dealer
from Hand import Hand
from Player import Player
from Shoe import Shoe


class Game(object):
    def __init__(self):
        self.shoe = Shoe(DECKS_IN_SHOE)
        self.players = []
        self.dealer = Dealer()

    def init_game(self):
        print(
            '''
            .------.
            |A_  _ |         Welcome to Ben's Blackjack Game
            |( \/ ).-----.    
            | \  /|J /\  |     Please follow the prompts below
            |  \/ | /  \ |
            `-----| \  / |
                  |  \/ J|
                  `------'
            '''
        )
        self.init_players()

    def init_players(self):
        player_count = get_non_negative_int_lt("How many players will be playing: ", 6)
        for i in range(1, int(player_count) + 1):
            name = input("Player %d name: " % i)
            self.players.append(Player(name))
        print('\n', end='')

    def play(self):
        while True:
            self.play_round()

    def play_round(self):
        self.take_bets()
        self.display_dealer()
        for player in self.players:
            print(f"\nIt is now {player.name}'s turn")
            self.play_hand(player)

        self.dealer.play(self.shoe)
        self.display_dealer()
        self.resolve_bets()
        self.display_money()
        self.kick_players()

    def take_bets(self):
        for player in self.players:
            bet_amount = get_non_negative_int_lt(
                f"How much would {player.name} like to bet? [Minimum: ${MINIMUM_BET}, Balance: {player.money}]: $",
                player.money, "You can not bet that amount!")
            if bet_amount < MINIMUM_BET:
                bet_amount = MINIMUM_BET
            player.money -= bet_amount
            player.set_hand(Hand([self.shoe.deal(), self.shoe.deal()], bet_amount))
        self.dealer.set_hand(Hand([self.shoe.deal(), self.shoe.deal()]))
        print('\n', end='')

    def display_dealer(self):
        print("Dealer's Hand:", self.dealer.hand)

    def play_hand(self, player):
        for i, hand in enumerate(player.hands):
            while not hand.busted() and not hand.stayed:
                print(f"\t{player.name}'s hand {i+1}\n\t", hand)
                choice = self.handle_hand_options(player, hand)

                if choice == 'Hit':
                    print(f"\t{player.name} chose to Hit!")
                    player.hit(hand, self.shoe)
                elif choice == 'Stay':
                    print(f"\t{player.name} chose to Stay!")
                    player.stay(hand)
                elif choice == "Double Down":
                    print(f"\t{player.name} chose to Double Down!")
                    player.double_down(hand, self.shoe)
                elif choice == "Split":
                    print(f"\t{player.name} chose to Split!")
                    player.split(hand)

            if hand.busted():
                print(f"\t{player.name}'s final hand {i+1} went bust\n\t", hand)
            else:
                print(f"\t{player.name}'s final hand {i+1}\n\t", hand)
            print('\n', end='')

    def handle_hand_options(self, player, hand):
        option_number = 1
        valid_options = []
        print('\tType the corresponding number:')
        print(f"\t\t[{option_number}] 'Stay'")
        valid_options.append('Stay')
        option_number += 1

        if hand.value < 21:
            print(f"\t\t[{option_number}] 'Hit'")
            valid_options.append('Hit')
            option_number += 1

        if hand.length() == 2 and hand.value != 21 and player.money > hand.bet and not hand.split_hand:
            print(f"\t\t[{option_number}] 'Double Down'")
            valid_options.append('Double Down')
            option_number += 1

        if hand.splitable() and len(
                [h for h in player.hands if h.split_hand]) <= SPLIT_LIMIT and player.money > hand.bet:
            print(f"\t\t[{option_number}] 'Split'")
            valid_options.append('Split')
            option_number += 1
        choice = get_non_negative_int_lt('\tChoice: ', max_val=option_number - 1, err="That is an invalid choice")
        print('\n', end='')
        return valid_options[choice - 1]

    def display_money(self):
        for player in self.players:
            print(f"{player.name} has ${player.money}")
        print("\n", end='')

    def resolve_bets(self):
        print(f"\tBetting Results:")
        dealer_value = self.dealer.hand.value
        dealer_blackjack = self.dealer.hand.blackjack()

        for player in self.players:
            for hand in player.hands:
                if not hand.busted() and hand.value > dealer_value:
                    player.money += hand.bet * WIN_MULTIPLIER
                    print(f"\t{player.name} won ${hand.bet * WIN_MULTIPLIER}")
                elif not hand.busted() and hand.value == dealer_value and not dealer_blackjack:
                    player.money += hand.bet
                    print(f"\t{player.name} pushed")
                else:
                    print(f"\t{player.name} lost his bet of ${hand.bet}")
        print('\n', end='')

    def kick_players(self):
        for player in self.players:
            if player.money == 0:
                self.players.remove(player)
                print(f"{player.name} has been eliminated")
                print("\n", end='')


def get_non_negative_int_lt(prompt, max_val=sys.maxsize, err="Sorry, I didn't understand that."):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(err)
            continue

        if value < 0 or value > max_val:
            print("Sorry, your response must be non-negative and <= %d" % max_val)
            continue
        else:
            break
    return value


if __name__ == "__main__":
    blackjack = Game()
    blackjack.init_game()
    blackjack.play()
