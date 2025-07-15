month_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
while True:
    try:
        n = input("Date: ").strip()
        n_orig = n
        if "/" in n:
            date = n.split("/")
            month = int(date[0])
            day = int(date[1])
            year = date[2]
            if month > 12 or day > 31:
                print("Please Enter A Valid Date")
                continue
        else:
            if "," not in n_orig:
                print("Missing comma.")
                continue
            date = n.replace(",","").split(" ")
            month = month_list.index(date[0]) + 1
            day = int(date[1])
            year = date[2]
        if day > 31:
            print("Please Enter A Valid Date")
            continue
        break
    except (EOFError, ValueError, IndexError):
        print("Invalid format. Please try again.")
d = str(day)
m = str(month)
if len(m) == 1:
    m = "0" + m
if len(d) == 1:
    d = "0" + d
print(year, m, d, sep = "-")



