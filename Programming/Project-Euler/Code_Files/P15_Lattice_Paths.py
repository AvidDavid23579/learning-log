c = [1]
n = 40
for k in range(n-1):
    next_val = (c[k] * (n-k)) / (k+1)
    c.append(next_val)

print(int(c[20]))
