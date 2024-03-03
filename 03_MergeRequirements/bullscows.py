import random


def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("guess should be the size of secret")
    
    bull_cnt = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bull_cnt += 1

    cow_cnt = len(set(guess).intersection(set(secret))) - bull_cnt
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


