import math
def largest_prime_factor(n):
    largest = -1
    while n % 2 == 0:
        largest = 2
        n //= 2
    for i in range(3, int(math.sqrt(n)), 2):
        while n % i == 0:
            largest = i
            n //= i
    if n > 1:
        largest = n
    return largest

print(largest_prime_factor(600851475143))
