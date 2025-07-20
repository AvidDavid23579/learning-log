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

morse = {
    "0":    "-----",
    "1":    ".----",
    "2":    "..---",
    "3":    "...--",
    "4":    "....-",
    "5":    ".....",
    "6":    "-....",
    "7":    "--...",
    "8":    "---..",
    "9":    "----.",
    "A":    ".-",
    "B":    "-...",
    "C":    "-.-.",
    "D":    "-..",
    "E":    ".",
    "F":    "..-.",
    "G":    "--.",
    "H":    "....",
    "I":    "..",
    "J":    ".---",
    "K":    "-.-",
    "L":    ".-..",
    "M":    "--",
    "N":    "-.",
    "O":    "---",
    "P":    ".--.",
    "Q":    "--.-",
    "R":    ".-.",
    "S":    "...",
    "T":    "-",
    "U":    "..-",
    "V":    "...-",
    "W":    ".--",
    "X":    "-..-",
    "Y":    "-.--",
    "Z":    "--..",
    " ":    "   "
}

def encryption_function(n):
    return n * (3 * n-1) // 2

n = input("Would you like to encrypt or decrypt? (E/D) ")

if n == "E":
    key = int(input("Please give me an encryption key "))

     #ERROR IS HERE IF WE WANT TO PARSE NON ALNUM CHARACTERS
    while True:
        try:
            input_text = input("Input text: ").upper()
            input_text = "".join(c for c in input_text if c.isalnum() or c == " ")
            if input_text.replace(" ","").isalnum():
                break  
            else:
                print("Only letters and numbers are allowed!")
        except EOFError:
            pass
    #ERROR IS HERE IF WE WANT TO PARSE NON ALNUM CHARACTERS


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
        encrypted_num = (encrypted_num + key + encryption_function(i)) % 27
        num_to_char = {v: k for k, v in conv.items()}
        output += num_to_char[encrypted_num]
        
    print("Encrypted output:", " ".join(morse.get(c, "") for c in output))


elif n == "D":
    key = int(input("Please give me a decryption key: "))
    morse_input = input("Input Morse Code: ").strip()

    morse_to_eng = {v: k for k, v in morse.items()}

    # Step 1: Morse → English letters
    words = morse_input.split("   ")  # 3 spaces = word break
    decoded_words = []
    for word in words:
        letters = word.split()  # 1 space = letter break
        decoded_word = "".join(morse_to_eng.get(letter, "") for letter in letters)
        decoded_words.append(decoded_word)

    decoded_text = " ".join(decoded_words)  # this is the Caesar-encrypted text

    # Step 2: Caesar decryption
    output = ""
    num_to_char = {v: k for k, v in conv.items()}
    for i, char in enumerate(decoded_text):
        decrypted_num = conv.get(char)
        decrypted_num = (decrypted_num - key - encryption_function(i)) % 27
        output += num_to_char[decrypted_num]

    print("Decrypted output:", output)




    

