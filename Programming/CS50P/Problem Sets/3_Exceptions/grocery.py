input_text = ""
while True:
    try:
        line = input().upper()
        if not line:
            break
        input_text += line + "\n"
    except EOFError:
        break

lines = input_text.splitlines() #list of lines

sorted_lines = sorted(set(lines))
for line in sorted_lines:
    print(lines.count(line), line)


