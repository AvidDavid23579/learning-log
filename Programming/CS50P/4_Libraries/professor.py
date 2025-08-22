import random
import sys


def main():
    n = get_level()
    score = 0
    for _ in range(10):
        x = generate_integer(n)
        y = generate_integer(n)
        error_count = 0
        while error_count < 3:
            try:
                result = int(input(f"{x} + {y} = "))
            except ValueError:
                print("EEE")
                error_count += 1
                continue
            if x + y == result:
                score += 1
                break
            else:
                print("EEE")
                error_count += 1
        if error_count == 3:
            print(f"{x} + {y} = {x+y}")
        error_count = 0
    print(f"Score: {score}")

    sys.exit()


def get_level():
    while True:
        n = input("Level: ")
        try:
            n = int(n)
            if 0 < n < 4:
                return n
            else:
                continue
        except ValueError:
            continue


def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)
    else:
        raise ValueError


if __name__ == "__main__":
    main()
