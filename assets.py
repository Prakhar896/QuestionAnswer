from main import *

def fileContent(fileName, passAPIKey=False):
    with open(fileName, "r") as f:
        f_content = f.read()
        if passAPIKey:
            f_content = f_content.replace("\{{ API_KEY }}", os.environ["API_KEY"])
            return f_content
        return f_content

@app.route("/assets/NYPAILogo")
def nypAILogo():
    return send_from_directory("assets", "NYPAILogo.jpg")

@app.route("/assets/copyright")
def copyrightJS():
    return fileContent("copyright.js")

@app.route("/assets/indexJS")
def indexJS():
    return fileContent("supportJSFiles/index.js")