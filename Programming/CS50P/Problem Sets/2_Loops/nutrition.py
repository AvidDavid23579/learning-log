def main():
    calories = {
        "apple": 130,
        "avocado": 50,
        "kiwifruit": 90,
        "pear": 100,
        "sweet cherries": 100,
    }

    fruit = input("Item: ").strip().lower()

    if fruit in calories:
        print(f"Calories: {calories[fruit]}")

main()
