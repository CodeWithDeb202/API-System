import sys


def show_menu():
    print("=> LinkedIn & Gmail Automation System")
    print("=> Enter 1, Setup / Test LinkedIn Log in session")
    print("=> Enter 2, Run LinkedIn Scraper (Past 24 Hours)")
    print("=> Enter 3, To Send  Personalizes email to recruiters")
    print("=> Enter 4, Check Gmail Inbox Replies (IMAP)")
    print("=> Enter 5, To Quite this pipeline")

def main():
    while True:
        show_menu()
        enter_num = input("Enter option (1-5): ").strip()

        if enter_num == "1":
            print("Helo 1")
        elif enter_num == "2":
            print("Hii 2")
        elif enter_num == "3":
            print("Helo 3")
        elif enter_num == "4":
            print("Helo 4")
        elif enter_num == "5":
            print("Quiting pipeline")
            sys.exit(0)
        else:
            print("Invaild option. Try again, Please Enter correct option which is over here")