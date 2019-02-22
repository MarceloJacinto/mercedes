#!/usr/bin/env python
#chmod +x main.py
from parser import Configurations
from functionality import *


def main():
    #1st -> Check the input args
    #    -> Load the config file
    configuration = Configurations()
    functions = Functionality(configuration)

    if configuration.mainArgument == "poll":
        functions.poll()
    elif configuration.mainArgument == "fetch":
        functions.fetch()
    elif configuration.mainArgument == "history":
        functions.history()
    elif configuration.mainArgument == "backup":
        functions.backup()
    elif configuration.mainArgument == "restore":
        a = 1
    elif configuration.mainArgument == "services":
        functions.printServices()
    elif configuration.mainArgument == "help":
        functions.help()
    elif configuration.mainArgument == "status":
        a = 1
    else:
        functions.help()


if __name__ == "__main__":
    main()
