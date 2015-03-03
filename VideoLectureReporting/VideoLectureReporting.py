
from FirstTimeDataTransformations import VideoViewTable
from Helpers import *

def welcome_msg():
    print """

     _   _ ___________ ______        _____  _____  __  
    | | | |_   _|  _  \___  /       |  _  ||  _  |/  | 
    | | | | | | | | | |  / /  __   _| |/' || |/' |`| | 
    | | | | | | | | | | / /   \ \ / /  /| ||  /| | | | 
    \ \_/ /_| |_| |/ /./ /___  \ V /\ |_/ /\ |_/ /_| |_
     \___/ \___/|___/ \_____/   \_/  \___(_)\___/ \___/
                                                                                                                                                     
    Welcome to the Video Lecture Reporting Command Line Interface.

    Here you can perform first time data munging operations for new data,
    produce reports for new data or old data, and perform a bunch of other 
    features I probably will never implement.

    Please choose an option:

    1) Perform first time data munging operations
    2) Generate a report
    3) See something cool
    4) Exit the program
    
    """

    choice = raw_input(">>> ")

    if choice == "1":
        #db_name = raw_input("\nDatabase name: ")
        #v = VideoViewTable(db_name)
        v = VideoViewTable()
        v.choose_database()
        v.CreateVideoViewTable()
        raw_input("    Press any key to continue . . .")
        welcome_msg()

    elif choice == "2":
        print "    this feature has not been implemented"
        raw_input("\n    Press any key to continue . . .\n")

        welcome_msg()

    elif choice == "3":
        p = Picard()
        p.get_picard()
        raw_input("    Press any key to continue . . .")
        welcome_msg()

    elif choice == "4":
        print "\n    Goodbye.\n"
        


if __name__ == "__main__":

    welcome_msg()
