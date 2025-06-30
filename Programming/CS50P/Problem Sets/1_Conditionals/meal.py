def main():
    t = input("What time is it? ")
    time = convert(t)
    if 7 <= time <= 8:
        print("breakfast time")
    elif 12 <= time <= 13:
        print("lunch time")
    elif 18 <= time <= 19:
        print("dinner time")
    else:
        return

def convert(time):
    if time.endswith("a.m"):
        hour = float(time.replace("a.m", "").split(":")[0])
        minute = float(time.replace("a.m", "").split(":")[1])
        if hour == 12:
            hour = 0
        return hour + minute / 60
    elif time.endswith("p.m"):
        hour = float(time.replace("p.m", "").split(":")[0])
        minute = float(time.replace("p.m", "").split(":")[1])
        if hour == 12:
            hour = 0
        return hour + minute / 60 + 12
    else:
        hour = float(time.split(":")[0])
        minute = float(time.split(":")[1])
        return hour + minute / 60 

if __name__ == "__main__":
    main()
