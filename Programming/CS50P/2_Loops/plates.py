def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    # Rule 1: Length must be between 2 and 6
    if not (2 <= len(s) <= 6):
        return False
    # Rule 2: First two characters must be letters
    if not (s[0].isalpha() and s[1].isalpha()):
        return False
    # Rule 3: Must be alphanumeric only
    if not s.isalnum():
        return False
    # Rule 4 & 5: Numbers must be at the end, and first number cannot be 0
    for i, c in enumerate(s):
        if c.isdigit():
            if c == '0':
                # First digit cannot be zero
                return False
            # All characters after this must be digits
            if not s[i:].isdigit():
                return False
            break
    return True
main()
