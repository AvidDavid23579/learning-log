menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}
total = 0
menu = {k.lower().strip(): v for k, v in menu.items()}

while True:
    try:
        n = input("Item: ").lower().strip()
        total += menu[n]
        print(f"Total: $", f"{total:.2f}", sep = "")
    except KeyError:
        continue
    except EOFError:
        print("Thanks for shopping!")
        break



