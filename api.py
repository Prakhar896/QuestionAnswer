from main import *

@app.route("/api/login", methods=["POST"])
def loginAccount():
    global data

    ## Check headers
    if "Content-Type" not in request.headers:
        return "ERROR: Content-Type header is not present."
    if request.headers["Content-Type"] != "application/json":
        return "ERROR: Content-Type header is not application/json."
    if "Key" not in request.headers:
        return "ERROR: Key header is not present."
    if request.headers["Key"] != os.environ["API_KEY"]:
        return "ERROR: Key header is not valid."
    

    ## Check body
    if "pass" not in request.json:
        return "ERROR: Password not present in request body."
    if request.json["pass"] != os.environ["ADMIN_PASS"]:
        return "UERROR: Invalid password."
    
    ## Success
    data["loggedInToken"] = generateToken()
    saveToFile(data)

    return "SUCCESS: Logged in; Token: {}".format(data["loggedInToken"])