"""
File: hangman.py
Name: Yu wen
-----------------------------
This program plays hangman game.
Users see a dashed word, trying to correctly figure the un-dashed word out by inputting one character each round.
If the user input is correct, show the updated word on console.
Players have N_TURNS chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    TODO: This program plays hangman game by replacing dashed word with correct guess.
    """

    word = random_word()
    ans = '-' * len(word)
    # for i in range(len(word)):
    #     ans = ans + '-'
    print(f'The word looks like: {ans}\nYou have {N_TURNS} wrong guesses left.')

    turns = N_TURNS
    while True:
        input_ch = input('Your guess: ').upper()
        if not input_ch.isalpha():
            print('Illegal format.')
        elif len(input_ch) > 1:
            print('Illegal format.')
        elif word.find(input_ch) == -1:
            turns = turns - 1
            print(f"There's no {input_ch}'s in the word.")
            if turns > 0:
                print(f'The word looks like: {ans}')
                print(f'You have {turns} wrong guesses left.')
            else:
                print('You are completely hung :(')
                break
        else:
            for i in range(len(word)):
                if word[i] == input_ch:
                    ans = ans[:i] + input_ch + ans[i+len(input_ch):]
            print('You are correct!')
            if ans != word:
                print(f'The word looks like: {ans}')
                print(f'You have {turns} wrong guesses left.')
            else:
                print(f'You win!!\nThe answer is: {word}')
                break


def random_word() -> str:
    """
    This function provides random word as the answer in the hangman game.
    """

    num = random.choice(range(10))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"
    elif num == 9:
        return 'AVAILABLE'


if __name__ == '__main__':
    main()
