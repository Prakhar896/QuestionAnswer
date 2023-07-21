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