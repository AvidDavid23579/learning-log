import math

def main():
    i = float(input("Find the sum of all the multiples of 3 or 5 below "))
    print("The sum of all the multiples of 3 or 5 below", i, "is", int(3 * asum(math.floor((i-1) / 3)) + 5 * asum(math.floor((i-1) / 5)) - 15 * asum(math.floor((i-1) / 15))))

def asum(a):
    return a*(a+1)/2 
    
if __name__ == "__main__":
    main()