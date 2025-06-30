ans = input("What is the Answer to the Great Question of Life, the Universe, and Everything? ")
if ans.strip() == "42":
    print("Yes")
elif ans.lower().replace("-", " ").strip() == "forty two":
    print("Yes")
else:
    print("No")
