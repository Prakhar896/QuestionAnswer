import os, sys, time

print("Welcome to the QuestionAnswer setup script!")
print("This script is meant to guide you through setting up QuestionAnswer.")
print("Please wait while I check the current system environment...")
time.sleep(1)

## Check python version
print()
print("Checking Python version...")
time.sleep(2)
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    print("ERROR: Python version is too low. Please use Python 3.8 or higher. You can visit https://www.python.org/downloads/ to download the latest version.")
    sys.exit(1)

## Check that flask, flask_cors and python-dotenv are installed
print()
print("Checking installation of required dependencies...")
time.sleep(2)
try:
    import flask
    import flask_cors
    import dotenv
except:
    print()
    print("One or more dependencies are not installed. Attempting to install from requirements.txt file...")
    if os.path.isfile(os.path.join(os.getcwd(), "requirements.txt")):
        os.system("pip install -r requirements.txt")
        print("Dependencies installed successfully.")
    else:
        print("ERROR: requirements.txt file not found. Please install dependencies (flask, flask-cors and python-dotenv) manually.")
        sys.exit(1)


## Check presence of .env file
print()
print("Checking for .env file and environment variables...")
time.sleep(2)
requiredList = ['APP_SECRET_KEY', 'API_KEY', 'ADMIN_PASS']
if os.path.isfile(os.path.join(os.getcwd(), ".env")):
    print()
    print(".env file found. Checking for required environment variables...")
    time.sleep(1)
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.split("=")[0] in requiredList:
                requiredList.remove(line.split("=")[0])
    if len(requiredList) > 0:
        print("ERROR: .env file does not contain all required environment variables. Please add the following variables to your .env file:")
        count = 1
        for variable in requiredList:
            print("\t{}. {}".format(count, variable))
            count += 1
        sys.exit(1)
    else:
        print("All required environment variables found.")
else:
    print()
    print(".env file not found. Initiating interactive .env file creation process...")
    time.sleep(1)
    fileContent = ""
    for variable in requiredList:
        if fileContent == "":
            fileContent += "{}={}".format(variable, input("\tEnter value for variable '{}': ".format(variable)))
        else:
            fileContent += "\n{}={}".format(variable, input("\tEnter value for variable '{}': ".format(variable)))
    
    print()
    print("Writing .env file...")
    with open(".env", "w") as f:
        f.write(fileContent)
    print(".env file written successfully.")
    time.sleep(1)

print()
print()
print("Setup operations completed successfully! You can now run QuestionAnswer by running the command 'python main.py' in the terminal.")