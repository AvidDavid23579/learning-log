def percentage(a, b):
    return round(a / b * 100)

while True:
    try:
        n = input("Fraction: ")
        num, den = map(int, n.split("/"))
        if num > den or num < 0:
            continue
        fuel = percentage(num, den)
        if fuel >= 99:
            print("F")
        elif fuel <= 1:
            print("E")
        else:
            print(f"{fuel}%")
        break
    except ZeroDivisionError:
        print("You can't divide by 0.")
    except ValueError:
        print("Please enter a positive number.")
    except IndexError:
        print("Please enter a fraction.")
