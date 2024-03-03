import random
import argparse
import os

from urllib.request import urlopen


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("guess should be the size of secret")

    bull_cnt = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bull_cnt += 1

    cow_cnt = len(set(guess).intersection(set(secret))) - bull_cnt
    print(guess)
    print(secret)
    return bull_cnt, cow_cnt


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        guess = input(prompt)
        if valid and (guess in valid):
            break
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    if not words:
        return 0

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
            print(e)
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
    print("You win! Attempts number: {}".format(gameplay(ask, inform, words)))
