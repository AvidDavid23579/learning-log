import random

while True:
    n = input("Level: ")
    try:
        n = int(n)
        if n > 0:
            break
        else:
            continue
    except ValueError:
        continue

goal = random.randint(1,n)

while True:
    g = input("Guess: ")
    try:
        g = int(g)
        if g <= 0:
            continue
        else:
            if g > goal:
                print("Too large!")
            elif g < goal:
                print("Too small!")
            else:
                print("Just right!")
                break
    except ValueError:
        continue

