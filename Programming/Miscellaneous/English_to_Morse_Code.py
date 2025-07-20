conv = {
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
while True:
    try:
        i = input("Would you like to convert from English to Morse Code or vice versa? (Type 'E' for English to Morse, 'M' for Morse to English): ").strip().upper()
        if i not in ['E', 'M']:
            raise ValueError("Invalid input")
        break 
    except ValueError as err:
        print("Invalid character. Please try again.")

if i == 'E':
    n = input("Input text: ").upper()
    print(" ".join(conv.get(c, "") for c in n))
elif i == 'M':
    morse_to_eng = {v: k for k, v in conv.items()}
    n = input("Input Morse Code: ").strip()
    words = n.split("   ")  # 3 spaces = word break
    decoded_words = []
    for word in words:
        letters = word.split()  # 1 space between letters
        decoded_word = "".join(morse_to_eng.get(letter, "") for letter in letters)
        decoded_words.append(decoded_word)
    print(" ".join(decoded_words))
   
