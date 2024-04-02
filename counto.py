#!/usr/bin/python3


import random
import time
import os


class Counto:
    def __init__(self):
        self.__num_rounds = 5
        self.__time_between_rounds = 2
        self.__min_integer = 1
        self.__max_integer = 9
        self.__total = 0

    @property
    def num_rounds(self):
        return self.__num_rounds

    @num_rounds.setter
    def num_rounds(self, new_num_rounds):
        self.__num_rounds = new_num_rounds

    @property
    def time_between_rounds(self):
        return self.__time_between_rounds

    @time_between_rounds.setter
    def time_between_rounds(self, new_time):
        self.__time_between_rounds = new_time

    @property
    def total(self):
        return self.__total

    def roll(self):
        num = random.randint(self.__min_integer, self.__max_integer)
        if random.random() < 0.5:
            num = -num
        self.__total += num
        return num

    def reset(self):
        self.__total = 0


class TerminalView:
    def __init__(self):
        pass

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def menu(self):
        print("\n\tMenu")
        print("\t1. Play Game")
        print("\t2. Settings")
        print("\t0. Exit")
        option = int(input("\tEnter option: "))
        return option

    def countdown(self):
        self.clear_screen()

        i = 3
        while i > 0:
            print("\n\n" + "COUNTDOWN".center(80), end="\n\n")
            print(f"{i}".center(80), end="\n\n")
            i -= 1
            time.sleep(1)
            self.clear_screen()

    def display_num(self, value, n, round_idx):
        print(f"\n\n\t\t\t\tRound: {round_idx}", end="\n\n\n")
        print(f"\t\t\t\t{value}")
        time.sleep(n)
        self.clear_screen()

    def guess_num(self):
        guess = int(input("\n\tGuess total: "))
        return guess

    def validate_result(self, guess, total):
        if guess == total:
            print("\tCorrect!")
        else:
            print("\tWrong!")
            print(f"\tTotal: {total}")

    def settings_menu(self):
        print("\n\t1. Set number of rounds")
        print("\t2. Set time between rounds")
        print("\t3. View Existing Settings")
        print("\t0. Return to Main Menu")
        option = int(input("\n\tChoose option: "))
        return option

    def define_num_rounds(self, cur_num_rounds):
        print(f"\tCurrent number of rounds: {cur_num_rounds}")
        num_rounds = int(input("\tEnter new number of rounds: "))
        return num_rounds

    def define_time_between_rounds(self, cur_time):
        print(f"\tCurrent time between rounds: {cur_time}")
        new_time = float(input("\tEnter time between rounds: "))
        return new_time

    def print_settings(
        self, num_rounds, time_between_rounds
    ):
        print('\n\tCurrent Settings')
        print(f"\tNumber of rounds: {num_rounds}")
        print(f"\tTime between rounds: {time_between_rounds}")

    def end_game(self):
        print("\tEnd Game", end="\n\n")

    def invalid_option(self):
        print("\n\tInvalid option. Please try again.")

    def value_error(self):
        print("\n\tPlease enter a valid value.\n")

    def non_positive_error(self):
        print("\n\tPlease enter a positive integer.")


class Controller:
    def __init__(self, game, view):
        self.g = game
        self.v = view
        self.gameloop()

    def gameloop(self):
        while True:
            while True:
                try:
                    option = self.v.menu()
                    if option not in (0, 1, 2):
                        raise InvalidOptionError

                except InvalidOptionError:
                    self.v.invalid_option()
                    continue

                except ValueError:
                    self.v.value_error()
                    continue

                else:
                    break

            if option == 1:
                self.play()
            elif option == 2:
                self.settings()
            elif option == 0:
                break

            self.g.reset()

        self.v.end_game()

    def play(self):
        rounds = 1
        self.v.countdown()

        while rounds <= self.g.num_rounds:
            num = self.g.roll()

            self.v.display_num(num, self.g.time_between_rounds, rounds)
            rounds += 1

        self.guess = self.v.guess_num()
        self.v.validate_result(self.guess, self.g.total)

        return

    def settings(self):

        while True:
            while True:

                self.v.print_settings(
                    self.g.num_rounds,
                    self.g.time_between_rounds
                )

                try:
                    option = self.v.settings_menu()
                    if option not in range(0, 3 + 1):
                        raise InvalidOptionError

                except InvalidOptionError:
                    self.v.invalid_option()
                    continue

                except ValueError:
                    self.v.value_error()
                    continue

                else:
                    break

            if option == 1:

                while True:
                    try:
                        new_num_rounds = self.v.define_num_rounds(
                            self.g.num_rounds
                        )
                        if new_num_rounds < 0:
                            raise NonPositiveError

                        if type(new_num_rounds) != int:
                            raise NonIntegerError

                    except NonPositiveError:
                        self.v.non_positive_error()
                        continue

                    except NonIntegerError:
                        self.v.non_integer_error()
                        continue

                    except ValueError:
                        self.v.value_error()
                        continue

                    else:
                        self.g.num_rounds = new_num_rounds
                        break

            elif option == 2:

                while True:
                    try:
                        time_between_rounds = (
                            self.v.define_time_between_rounds(
                                self.g.time_between_rounds
                            )
                        )

                    except NonPositiveError:
                        self.v.non_positive_error()
                        continue

                    except ValueError:
                        self.v.value_error()
                        continue

                    else:
                        self.g.time_between_rounds = time_between_rounds
                        break

            elif option == 3:
                self.v.print_settings(
                    self.g.num_rounds,
                    self.g.time_between_rounds
                )
            elif option == 0:
                break

        return


class InvalidOptionError(Exception):
    """Raised when user inputs an invalid option."""


class NonPositiveError(Exception):
    """Raised when user inputs a nonpositive integer."""


if __name__ == "__main__":
    g = Counto()
    v = TerminalView()
    Controller(g, v)
