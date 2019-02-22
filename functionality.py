import requests
import csv
import threading
import _thread as thread
import time
import shutil
import os


class Functionality:

    def __init__(self, configuration):  
        self.test = 0
        self.config = configuration
        #Thread event useful for the fetch
        self.e = threading.Event()

        #List of status for the services
        self.currentStorage = []
        # Header to fool some website (like amazon) into thinking this is a browser
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}

    #Function to check if the services in the config file are up
    def poll(self):
        for key, value in self.config.services.items():
            data = requests.get(value, allow_redirects=True, timeout=(4, 16), headers=self.headers)
            #save the services in current Storage
            current = (key, data.headers['Date'], data.status_code)
            #print the current data in console
            self.printStatus(current)
            #saves in the storage file
            self.saveLocal([current])
            self.currentStorage.append(current)

    #Function to call poll multiple times in an external thread
    def fetch(self):
        
        t = threading.Thread(target=self.fetchHelper, name="thread1", args=())
        t.start()
            
        #Checks if program is exiting
        print('Press CTRL-C to interrupt')
        while t.isAlive():
            try: 
                time.sleep(1) #wait 1 second, then go back and ask if thread is still alive
            except KeyboardInterrupt: #if ctrl-C is pressed within that second,
                #catch the KeyboardInterrupt exception
                self.e.set() #set the flag that will kill the thread when it has finished
        print('Exiting...')
        t.join() #wait for the thread to finish
        print(self.currentStorage)
        
    #Helper function to run on the thread for the fetch
    def fetchHelper(self):
        while(True) and not self.e.isSet():
            self.poll()
            time.sleep(self.config.fetchDelay)
            thread.interrupt_main()

    def history(self):
        #Reading the storage file and saving into program storage
        try:  
            with open('storage.csv','r') as csvin:
                csv_in=csv.reader(csvin, delimiter=",")
                onlyServices = None
                if self.config.optionArguments["only"] != None:
                    onlyServices = list(map(str.strip, self.config.optionArguments["only"].split(',')))
                #verification of the only parameter here
                #NOT EFFICIENT O^2 -> To be corrected
                #Not critical, because only parameter takes few arguments
                for rows in csv_in:
                    if onlyServices:
                        for service in onlyServices:
                            if service in rows[0]:
                                self.currentStorage.append((rows[0], rows[1], rows[2]))
                    else:
                        self.currentStorage.append((rows[0], rows[1], rows[2]))
        except IndexError:
            print("Error in storage.csv")
        #Printing from the data from the variable
        for data in self.currentStorage:
            self.printStatus(data)

    #Implements copying the storage file to other location
    def backup(self):
        try:
            print(os.path.exists('Desktop/myfile.txt'))
            print(os.access(os.path.dirname('Desktop/myfile.txt'), os.W_OK))
            print(os.path.abspath('Desktop/myfile.txt'))
            shutil.copy(self.config.storageFileName, os.path.abspath('Desktop/myfile.txt'))
        except (FileExistsError, FileNotFoundError) as e:
            print(e)


    #Prints the status on the console
    def printStatus(self, data):
        print("[" + data[0] + "] " + data[1] + " - ", end="")
        if (str(data[2]) == "200"):
            print("up")
        else:
            print("down")

    #Prints services
    def printServices(self):
        for service, endpoint in self.config.services.items():
            print("[" + service + "] " + endpoint)

    #Save data to the local storage
    def saveLocal(self, data):
        with open(self.config.storageFileName,'a') as out:
            csv_out=csv.writer(out)
            #csv_out.writerow(['services','date','status'])
            for row in data:
                csv_out.writerow(row)

    #Prints the help guide
    def help(self):
        helpFile = open("help.txt", "r")
        print(helpFile.read())
        helpFile.close() 