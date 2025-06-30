g = input("Greeting: ")
if g.strip().lower().startswith("hello"):
    print("$0")
elif g.strip().lower().startswith("h"):
    print("$20")
else:
    print("$100")