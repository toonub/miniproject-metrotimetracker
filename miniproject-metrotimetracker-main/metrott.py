from datetime import datetime
import datetime as dt

f = open("metro.csv","r")
timings = f.readlines()
f.close

current_time= datetime.now()
y= int(datetime.now().strftime("%Y"))
m= int(datetime.now().strftime("%m"))
d= int(datetime.now().strftime("%d"))

for l in timings:
    h,min = l.strip().split(":")
    metro_time=datetime(y,m,d,int(h),int(min))
    walk=dt.timedelta(minutes=12)
    time_to_next_train=metro_time-current_time

    if time_to_next_train>=dt.timedelta(days=0):
        if time_to_next_train>=walk:

            hours,mins,sec = str(time_to_next_train).split('.')[0].split(':')
            print(f"The Next Train will arrive at {mins} mins {sec} seconds")
            break

        else:

            hours,mins,sec = str(time_to_next_train).split('.')[0].split(':')
            print(f"You have only {mins} mins {sec} seconds to reach the current train")



