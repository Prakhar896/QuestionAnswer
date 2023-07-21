import os, sys, json, shutil, datetime, random
from dotenv import load_dotenv
load_dotenv()


def fileContent(fileName, passAPIKey=False):
    with open(fileName, "r") as f:
        f_content = f.read()
        if passAPIKey:
            f_content = f_content.replace("\{{ API_KEY }}", os.environ["API_KEY"])
            return f_content
        return f_content
    

def generateToken():
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    token = list(str(datetime.datetime.now().timestamp()).replace(".", ""))
    for index in range(len(token)):
        if index % 2 == 0:
            token.insert(index, alphabets[random.randint(0, len(alphabets) - 1)])
    return "".join(token)

def saveToFile(data):
    with open("data.txt", "w") as f:
        json.dump(data, f)