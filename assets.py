from main import *

@app.route("/assets/NYPAILogo")
def nypAILogo():
    return send_from_directory("assets", "NYPAILogo.jpg")

@app.route("/assets/copyright")
def copyrightJS():
    return fileContent("copyright.js")

@app.route("/assets/indexJS")
def indexJS():
    return fileContent("supportJSFiles/index.js", passAPIKey=True)

@app.route("/assets/unansweredJS")
def unansweredJS():
    return fileContent("supportJSFiles/unanswered.js", passAPIKey=True)

@app.route("/assets/answeredJS")
def answeredJS():
    return fileContent("supportJSFiles/answered.js", passAPIKey=True)

@app.route("/assets/askJS")
def askJS():
    return fileContent("supportJSFiles/ask.js", passAPIKey=True)