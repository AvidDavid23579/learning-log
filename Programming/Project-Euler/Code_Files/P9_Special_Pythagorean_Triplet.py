# a = m**2 + n**2
# b = 2mn
# c = m**2 - n**2
# a + b + c = 2m**2 + 2mn
# (a + b + c) / 2 = m * (m + n) = 500
d1 = []
for i in range(500):
    if 500 % (i+1) == 0:
        d1.append(i+1)
d2 = d1[::-1]


for i in range(len(d1)):
    m = d1[i]
    n = (500 / m) - m

    a = m**2 - n**2
    b = 2*m*n
    c = m**2 + n**2
    if a**2 + b**2 == c**2 and a > 0 and b > 0 and c > 0:
        print(int(a*b*c))
        break

        
