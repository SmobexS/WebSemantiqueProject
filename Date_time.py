from datetime import *

def dateStringToDay(string):
    date = datetime.strptime(string, "%d-%m-%Y")
    return date.strftime("%A")  

def dateStringToTime(string):
    time = datetime.strptime(string, "%H:%M")
    return time.strftime("%H:%M")

def get_date_from_user() :
    valid_date = False

    while valid_date == False:
        date_string = input("Enter a date (dd-mm-yyyy) (Today by default if you press Enter) : ") or datetime.now().strftime("%d-%m-%Y")
        try:
            date_chek = datetime.strptime(date_string, "%d-%m-%Y")
            date_chek = date_chek.strftime("%d-%m-%Y")
            now = datetime.now().strftime("%d-%m-%Y")
            if date_chek < now :
                print("Invalid date format. Please try again.")
            else:
                valid_date = True
        except ValueError:
            print("Invalid date format. Please try again.")
    print("The chosen date is : ", date_string)
    day = dateStringToDay(date_string)
    
    return (day, date_string)

def get_time_from_user(date_string) :
    valid_time = False

    while valid_time == False:
        time_string = input("Enter a time (HH:MM) (Now by default if you press Enter) : ") or datetime.now().strftime("%H:%M")
        try:
            time_chek = datetime.strptime(time_string, "%H:%M")
            time_chek = time_chek.strftime("%H:%M")
            if time_chek < datetime.now().strftime("%H:%M") and date_string == datetime.now().strftime("%d-%m-%Y"):
                print("Invalid time format. Please try again.")
            else:
                valid_time = True
        except ValueError:
            print("Invalid time format. Please try again.")
    print("The chosen time is : ", time_string)
    time = dateStringToTime(time_string)
    
    return time