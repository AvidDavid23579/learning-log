import math
def sieve(n):
    # Step 1: Assume all numbers are prime
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime

    # Step 2: Cross out non-primes
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:  # if p hasn't been crossed out
            for multiple in range(p*p, n + 1, p):
                is_prime[multiple] = False

    # Step 3: Collect primes
    primes = [i for i, val in enumerate(is_prime) if val]
    return primes

n = 10001
m = int(n * math.log(n) + n * math.log(math.log(n)))
print(sieve(m)[n-1])