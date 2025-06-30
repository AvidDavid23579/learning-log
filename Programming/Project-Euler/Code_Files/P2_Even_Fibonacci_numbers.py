def main():
    i = int(input("Find the sum of even-valued Fibonacci numbers that do not exceed "))

    result = 0
    sum = 0
    prev1 = 1
    prev2 = 2
    while prev2 < i:
        if prev2 % 2 == 0:
            sum += prev2
        result = prev1 + prev2
        prev1 = prev2
        prev2 = result
    print(sum)

if __name__ == "__main__":
    main()