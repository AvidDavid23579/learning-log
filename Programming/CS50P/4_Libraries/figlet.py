import sys
import pyfiglet

if len(sys.argv) == 1:
    n = input("Input: ")
    print("Output:\n", pyfiglet.figlet_format(n))
elif len(sys.argv) == 3 and (sys.argv[1] == "-f" or sys.argv[1] == "--font"):
    try:
        pyfiglet.figlet_format("test", font=sys.argv[2])
        n = input("Input: ")
        print("Output:", pyfiglet.figlet_format(n, font=sys.argv[2]))
    except pyfiglet.FontNotFound:
        print("Invalid font")
        sys.exit(1)
else:
    print("Invalid usage")
    sys.exit(1)

