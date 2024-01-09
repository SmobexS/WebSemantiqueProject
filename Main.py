import sys
from Collect import *
from Describe import describe


def main ():
    
    thread = collect()
    if thread != None :
        
        thread.start()

        describe()


        if thread.is_alive() :

            validate = False
            while validate == False :
                des=input("The collect dataset programme is still running do you want to end it and exit the application (y/n): ")
                if des =="y":
                    validate = True
                    sys.exit(0)
                    
                elif des == "n":
                    validate = True
                
                else:
                    validate = False
                    print("Please chose 'y' for yes or 'n' for no.")
    
    else:
        
        describe()

if __name__ == "__main__":
    main()

