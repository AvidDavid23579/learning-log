n = str(input("camelCase: "))
result = ""
for i, c in enumerate(n):
    if  c.isupper():
        result += "_" + c.lower()
    else:
        result += c
print("snake_case:", result)