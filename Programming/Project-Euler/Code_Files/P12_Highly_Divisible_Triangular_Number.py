def triangle(n):
    return n * (n+1) // 2

def count_divisors(n):
    count = 0
    for i in range(1,int((n**0.5) + 1)):
        if n % i == 0:
            count += 2 if i != n // i else 1
    return count

n = 1
while True:
    t = triangle(n)
    if count_divisors(t) > 500:
        print(t)
        break
    n += 1

            
            

