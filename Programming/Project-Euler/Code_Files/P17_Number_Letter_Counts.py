from num2words import num2words
n = ""
for i in range(1,1001):
    n += num2words(i).strip().replace(" ", "").replace("-","")
print(i,len(n))

