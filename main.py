from tabulate import tabulate
import random
import os


def press_enter_to_continue():
    input("\nPress Enter to continue...")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Kingdom:
    def __init__(self, name, gold=10, army=1, population=2):
        # tax = 17
        self.name = name
        self.gold = gold
        self.army = army
        self.population = population

    def collect_taxes(self):
        self.gold += self.population // 10
        # - - - - -
        self.gold -= self.army * 2
        self.gold += self.population * 0.5

    def do_nothing(self):
        self.population += 5
        # - - - - -
        self.gold -= self.army * 2
        self.gold += self.population * 0.5

    def train_soldiers(self):
        if self.gold >= 10:
            self.gold -= 10
            self.population -= 5
            self.army += 5
            # - - - - -
            self.gold -= self.army * 2
            self.gold += self.population * 0.5
        else:
            print(f"{self.name}: Not enough gold to train soldiers.")

    def start_battle(self, opponent):
        clear_screen()
        attacking_army = self.army
        defending_army = opponent.army
        ratio = attacking_army / defending_army

        if attacking_army > defending_army:
            # Calculate percentage of defending army destroyed based on the ratio
            destruction_percentage = min(1.0, 0.25 * ratio)  # Cap at 100%
            loss = round(destruction_percentage * defending_army)
            opponent.army -= round(loss)
            self.army -= round(loss/2)  # bonus

            if self.name == "Player":
                print(f"\nYou attacked and destroyed {destruction_percentage:.0%} of the opponent's army ({loss} soldiers).")
            else:
                print(f"\nThe opponent attacked and destroyed {destruction_percentage:.0%} of your army ({loss} soldiers).")

        elif attacking_army < defending_army:
            # Similar calculation, but from the defender's perspective
            destruction_percentage = min(1.0, 0.25 / ratio)
            loss = round(destruction_percentage * attacking_army)
            self.army -= round(loss)
            opponent.army -= round(loss/2)  # bonus

            if self.name == "Player":
                print(f"\nYou defended and lost {destruction_percentage:.0%} of your army ({loss} soldiers).")
            else:
                print(f"\nThe opponent defended and lost {destruction_percentage:.0%} of their army ({loss} soldiers).")

        else:
            print("\nIt's a draw. Both armies lost.")
            loss = round(attacking_army / 2)
            opponent.army -= loss
            self.army -= loss
        if opponent.army <= 0:
            print("\nThe opponent's army has been defeated! You win!")
            exit()
        elif self.army <= 0:
            print("\nYour army has been defeated! it's over")
            exit()
        else:
            press_enter_to_continue()
            clear_screen()


class OpponentKingdom(Kingdom):
    def make_decision(self, player_kingdom):
        army_ratio = self.army / player_kingdom.army
        if self.gold < 50 and self.population > 10:
            return random.choice(["collect taxes", "do nothing"])
        elif self.army < 30 and self.population > 10:
            return random.choice(["train soldiers", "do nothing"])
        elif self.population < 30:
            return "do nothing"
        elif self.gold > 50 and self.army > 30 and self.population > 30 and army_ratio > 0.5 and random.random() < 0.1:
            return "start battle"
        elif self.gold > 50 and self.army > 30 and self.population > 30 and army_ratio > 1.5 and random.random() < 0.4:
            return "start battle"
        else:
            return random.choice(["collect taxes", "train soldiers", "do nothing"])


player_kingdom = Kingdom("Player")
opponent_kingdom = OpponentKingdom("Opponent")

while player_kingdom.army > 0 and opponent_kingdom.army > 0:
    player_data = [["Player Kingdom", player_kingdom.gold, player_kingdom.army, player_kingdom.population]]
    opponent_data = [["Opponent Kingdom", opponent_kingdom.gold, opponent_kingdom.army, opponent_kingdom.population]]

    # Print the table
    print("\n")
    print(tabulate(player_data + opponent_data, headers=["Kingdom", "Gold", "Army", "Population"]))

    # Player's turn
    while True:
        action_choice_table = tabulate([["Do nothing"], ["Collect Taxes"], ["Train Soldiers"], ["Start battle"]], headers=["Action:"])
        action = input(f"\n{action_choice_table}\n--------------\nYour action: ").lower()
        clear_screen()
        if action in ["do nothing", "0"]:
            player_kingdom.do_nothing()
            break
        elif action in ["collect taxes", "1"]:
            player_kingdom.collect_taxes()
            break
        elif action in ["train soldiers", "2"]:
            player_kingdom.train_soldiers()
            break
        elif action in ["start battle", "3"]:
            player_kingdom.start_battle(opponent_kingdom)
            break
        else:
            print("Invalid action. Please choose from the options provided.")

    # Opponent's turn
    opponent_action = opponent_kingdom.make_decision(player_kingdom)
    print("\n")
    print("Opponent Kingdom:", opponent_kingdom.name, "chooses to", opponent_action)
    press_enter_to_continue()
    if opponent_action == "collect taxes":
        opponent_kingdom.collect_taxes()
    elif opponent_action == "train soldiers":
        opponent_kingdom.train_soldiers()
    elif opponent_action == "start battle":
        opponent_kingdom.start_battle(player_kingdom)
    elif opponent_action == "do nothing":
        opponent_kingdom.do_nothing()
    clear_screen()
