import random
import argparse
import os

from urllib.request import urlopen
from collections import Counter
from io import StringIO
from cowsay import cowsay, read_dot_cow

def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("guess should be the size of secret")

    bulls, cows = 0, 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1

    guess_counter = Counter(guess)
    secret_counter = Counter(secret)

    for key in guess_counter:
        if key in secret_counter:
            cows += min(guess_counter[key], secret_counter[key])

    return bulls, cows - bulls


def ask(prompt: str, valid: list[str] = None) -> str:
    cow = read_dot_cow(StringIO("""
    $the_cow = <<EOC;
             $thoughts
              $thoughts
               ___
              (o o)
             (  V  )
            /--m-m-
    EOC
    """))
    while True:
        print(cowsay(prompt, cowfile=cow))
        guess = input()
        if guess in valid:
            break
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay(format_string.format(bulls, cows)))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = random.choice(words)
    attempt_cnt = 0

    while True:
        attempt_cnt += 1
        guess = ask("Введите слово: ", words)
        try:
            bulls, cows = bullscows(guess, secret)
        except ValueError:
            continue
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if bulls == len(secret):
            break
    return attempt_cnt


def read_dictionary(path: str, length: str) -> list[str]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            words = [
                word.strip() for word in file.readlines() if len(word.strip()) == length
            ]
    else:
        try:
            with urlopen(path) as file:
                words = [
                    word.decode("utf-8").strip()
                    for word in file.readlines()
                    if len(word.decode("utf-8").strip()) == length
                ]
        except Exception as e:
            print(f"{path} is not valid path or URL")
            exit()
    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", type=str, help="dictionary filename or URL")
    parser.add_argument(
        "length", nargs="?", default=5, type=int, help="length of words"
    )

    args = parser.parse_args()

    words = read_dictionary(args.dictionary, args.length)
    if len(words) == 0:
        print("Dictionary is empty")
    else:
        print("You win! Attempts number: {}".format(gameplay(ask, inform, words)))
