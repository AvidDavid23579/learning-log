inp = input("Input: ")
result = ""
for i, c in enumerate(inp):
    if c in ("a","e","i","o","u","A","E","I","O","U"):
        result += ""
    else:
        result += c
print("Output", result)


