import datetime, time

##TODO: Fix for past dates.
##TODO: Probably completely rethink this entire thing.

def howlong(event):
    print('howlong')
    if type(event).__name__ == 'str':
        cur_yr = datetime.datetime.now().year
        type(cur_yr)
        crimbo_date = datetime.datetime(cur_yr, 12, 24, 17, 30, 0)
        halloween = datetime.datetime(cur_yr, 10, 31, 00, 01, 0)
        thatdate = datetime.datetime(cur_yr, 11, 11, 11, 11, 11)
        newyear = datetime.datetime((cur_yr + 1), 01, 01, 00, 00, 1)
    elif type(event).__name__ == 'list':
        day = int(event[0])
        month = int(event[1])
        year = int(event[2])
        custom_date = datetime.datetime(year, month, day, 00, 01, 0)
    else:
        print("No luck with howlong.")
        return None
    
    now_date = datetime.datetime.now()
    if event == "xmas":
        diff = crimbo_date - now_date
        blah = "odd seconds left to shop for Christmas. BUY NOW!"
    elif event == "halloween":
        diff = halloween - now_date
        blah = "seconds left to halloween."
    elif event == "newyear":
        diff = newyear - now_date
        blah = "seconds left of %d, dust off those party hats." % (cur_yr)
    else:
        diff = custom_date - now_date
        blah = "seconds and counting down..."
        print(event)
        
    weeks, days = divmod(diff.days, 7)
    mins, secs = divmod(diff.seconds, 60)
    hours, mins = divmod(mins, 60)
    
    if weeks < 0:
        weeks = 54 + weeks

    return weeks,days,hours,mins,secs,blah


if __name__ == "__main__":
    input = "halloween"
    weeks,days,hours,mins,secs,blah = howlong(input)
    out = ["There are only %d weeks, %d days, %d hours, %d minutes and %d %s" % (weeks,days,hours,mins,secs,blah)]
    print(out)
