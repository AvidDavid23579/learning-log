import math

def count_divisors(n):
    count = 1
    i = 2
    while i * i <= n:
        power = 0
        while n % i == 0:
            n //= i
            power += 1
        count *= (power + 1)
        i += 1
    if n > 1:
        count *= 2
    return count

def triangle_with_divisors(limit):
    n = 1
    while True:
        if n % 2 == 0:
            d1 = count_divisors(n // 2)
            d2 = count_divisors(n + 1)
        else:
            d1 = count_divisors(n)
            d2 = count_divisors((n + 1) // 2)
        
        if d1 * d2 > limit:
            return n * (n + 1) // 2
        n += 1

print(triangle_with_divisors(500))


            
            

