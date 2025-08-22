n = 50  # Amount Due
while n > 0:
        i = int(input("Amount Due: " + str(n) + "\nInsert Coin: "))
        if i in (25, 10, 5):
            n -= i
if n <=0:
    print("Change Owed:", abs(int(n)))