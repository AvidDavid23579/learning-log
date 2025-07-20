from num2words import num2words

conv = {
    " ": 0,
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 11,
    "L": 12,
    "M": 13,
    "N": 14,
    "O": 15,    
    "P": 16,
    "Q": 17,
    "R": 18,
    "S": 19,
    "T": 20,
    "U": 21,
    "V": 22,
    "W": 23,
    "X": 24,
    "Y": 25,
    "Z": 26,
}


n = input("Would you like to encrypt or decrypt? (E/D) ")

if n == "E":
    key = int(input("Please give me an encryption key "))
    while True:
        try:
            input_text = input("Input text: ").upper()
            if input_text.replace(" ","").isalnum():
                break  
            else:
                print("Only letters and numbers are allowed!")
        except EOFError:
            pass

    input_parsed = ""


    for char in input_text:
        if char.isdigit():
            input_parsed += num2words(int(char)).upper() + " "
        else:
            input_parsed += char 


    output = ""

    for i in range(len(input_parsed)):
        char = input_parsed[i]
        encrypted_num = conv.get(char)
        encrypted_num = (encrypted_num + key + i) % 27
        num_to_char = {v: k for k, v in conv.items()}
        output += num_to_char[encrypted_num]

    print("Encrypted output:", output)

elif n == "D":
    key = int(input("Please give me a decryption key "))

    while True:
        try:
            input_text = input("Input text: ").upper()
            if input_text.replace(" ","").isalnum():
                break  
            else:
                print("Only letters and numbers are allowed!")
        except EOFError:
            pass

    output = ""

    for i in range(len(input_text)):
        char = input_text[i]
        decrypted_num = conv.get(char)
        decrypted_num = (decrypted_num - key - i) % 27
        num_to_char = {v: k for k, v in conv.items()}
        output += num_to_char[decrypted_num]

    print("Decrypted output:", output)


    

