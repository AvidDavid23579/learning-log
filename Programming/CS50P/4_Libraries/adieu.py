name_list = []
while True:
    try:
        line = input("Name: ")
        if not line:
            break
        name_list.append(line)
    except EOFError:
        print()
        break

if len(name_list) == 1:
    print("Adieu, adieu, to", name_list[0])
elif len(name_list) == 2:
    print("Adieu, adieu, to", name_list[0], "and", name_list[1])
else:
    s = ""
    for name in name_list:
        if name != name_list[-1]:
            s += (name + ", ")
        else:
            s += "and " + name
    print("Adieu, adieu, to", s)


