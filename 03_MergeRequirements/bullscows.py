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


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    pass

