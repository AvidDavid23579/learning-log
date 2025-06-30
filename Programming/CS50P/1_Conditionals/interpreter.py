e = input("Expression: ").split(" ")
if e[1] == "+":
    print(float(e[0]) + float(e[2]))
elif e[1] == "-":
    print(float(e[0]) - float(e[2]))
elif e[1] == "*":
    print(float(e[0]) * float(e[2]))
elif e[1] == "/":
    print(float(e[0]) / float(e[2]))