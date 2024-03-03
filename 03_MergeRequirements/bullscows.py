def bullscows(guess: str, secret: str) -> (int, int):
    if len(guess) != len(secret):
        raise ValueError("guess should be the size of secret")
    
    bull_cnt = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bull_cnt += 1

    cow_cnt = len(set(guess).intersection(set(secret))) - bull_cnt
    return bull_cnt, cow_cnt


if __name__ == "__main__":
    guess = input()
    secret = input()
    print(bullscows(guess, secret))
