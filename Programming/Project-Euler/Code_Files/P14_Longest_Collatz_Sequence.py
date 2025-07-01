def collatz(n, memo):
    original = n
    steps = 0
    while n != 1:
        if n in memo:
            steps += memo[n]
            break
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n+1
        steps +=1
    memo[original] = steps
    return steps

def main():
    memo = {}
    length = 0
    result = 0
    for i in range(1,1000000):
        c = collatz(i, memo)
        if c > length:
            length = c
            result = i
    print(result, length) 
        

main()