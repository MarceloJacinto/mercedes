import sys
import argparse
import csv

#Class that contains all methods to check,
#the arguments passed in the console
class Configurations:

    def __init__(self):
        self.storageFileName = "storage.csv"
        self.configFileName = "config.txt"
        #dictionary with services and their url
        self.services = None

        #delay for the fetch
        self.fetchDelay = 5

        #main argument such as: "poll, fetch, ..." and validates it
        self.mainArgument = None
        self.validateMainArgument()
        print(self.mainArgument)

        #dictionary with the optional arguments parsed in console
        self.optionArguments = vars(self.create_parser(sys.argv[2:]))
        print(self.optionArguments)

        #Validates the combination of main argument and optional arguments
        self.validateCombinationArguments()

        #After arguments validation reads the configuration file
        self.ReadConfigFile()

        #Remove the unwanted services
        self.removeUnwantedServices()

    #Reads the configuration file, and saves the data in dictionary named services
    def ReadConfigFile(self):
        try:
            with open(self.configFileName, 'r') as csvfile:
                listOfServices = csv.reader(csvfile, delimiter='|')
                self.services = {rows[0]:rows[1] for rows in listOfServices}
                print(self.services)
        except IndexError:
            print("Error in config.txt")

    #Function to validate the main argument
    def validateMainArgument(self):
        if len(sys.argv) >= 2:
            validArguments = ["poll","fetch","history", "backup", "restore", "services", "help", "status"]
            for argument in validArguments:
                if sys.argv[1] == argument:
                    self.mainArgument = argument
                    return
            print("Invalid argument!")
            exit()

    #Creates a parser for the optional arguments
    def create_parser(self, args):
        parser = argparse.ArgumentParser(description='options')
        parser.add_argument('--refresh', help='update the refresh rate of fetch', type=int)
        parser.add_argument('--only', help='only updates status of choosen service', type=str)
        parser.add_argument('--exclude', help='doesnt update the status of the excluded service', type=str)
        parser.add_argument('--format', help='To save the local storage to a file of specific format', type=str)
        parser.add_argument('--merge', help='To append the local storage to a file', type=bool)
        args = parser.parse_args(args)
        print(args)
        return args

    #Validates the main arguments with the optional arguments
    def validateCombinationArguments(self):
        #if there are optional arguments
        if len(sys.argv) > 2:
            if self.optionArguments["only"] != None and self.optionArguments["exclude"] != None:
                print("Doesn't make sense! Use only and exclude separatly")
                exit()
            elif self.mainArgument == "help" or self.mainArgument == "services" or self.mainArgument == "status":
                for key, value in self.optionArguments.items():
                    if value != None:
                        print("Help command doesn't take any optional arguments!")
                        exit()
            elif self.mainArgument == "poll":
                for key, value in self.optionArguments.items():
                    if (key != "only" and key != "exclude") and value!= None:
                        print("Optional argument not valid with this main argument")
                        exit()
            elif self.mainArgument == "fetch":
                for key, value in self.optionArguments.items():
                    if key == "refresh":
                        if value < 6:
                            print("Refresh rate must be bigger than 5 seconds!")
                            exit()
                        else:
                            self.fetchDelay = value
                    if (key != "only" and key != "exclude" and key !="refresh") and value!= None:
                        print("Optional argument not valid with this main argument")
                        exit()
            elif self.mainArgument == "history":
                for key, value in self.optionArguments.items():
                        if key != "only" and value!= None:
                            print("Optional argument not valid with this main argument")
                            exit()
            elif self.mainArgument == "backup":
                for key, value in self.optionArguments.items():
                        if key != "format" and value!= None:
                            print("Optional argument not valid with this main argument")
                            exit()
            elif self.mainArgument == "restore":
                for key, value in self.optionArguments.items():
                        if key != "merge" and value!= None:
                            print("Optional argument not valid with this main argument")
                            exit()

    #Removes the unwanted URLs from the services dictionary
    def removeUnwantedServices(self):
        if self.optionArguments["only"] != None:
            onlyServices = list(map(str.strip, self.optionArguments["only"].split(',')))
            #Creates the dictionary of services
            auxDic = {auxService: None for auxService in onlyServices}
            #Only hads the webstite from the original services for the ones choosen
            for key, value in auxDic.items():
                if key in self.services:
                    auxDic[key] = self.services[key]
            #Clears the services
            self.services = {}
            #updates the services dictionary
            #This setp is only for verification purposes
            for key, value in auxDic.items():
                if value != None:
                    self.services.update({key: value})
            print(self.services)
        elif self.optionArguments["exclude"] != None:
            print(self.optionArguments["exclude"])
            excludedServices = list(map(str.strip, self.optionArguments["exclude"].split(',')))
            for i in excludedServices:
                if i in self.services:
                    self.services.pop(i)
            print(self.services)