from main import *

@app.route("/assets/NYPAILogo")
def nypAILogo():
    return send_from_directory("assets", "NYPAILogo.jpg")

