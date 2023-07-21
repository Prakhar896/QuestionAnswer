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

@app.route("/api/requestQuestionData", methods=['POST'])
def requestQuestionData():
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
    if "token" not in request.json:
        return "ERROR: Token not present in request body."
    if request.json["token"] != data["loggedInToken"]:
        return "ERROR: Invalid token."
    if 'filter' not in request.json:
        return "ERROR: Filter not present in request body."
    if request.json["filter"] not in ["all", "unanswered", "answered"]:
        return "ERROR: Invalid filter."
    
    filter = request.json['filter']

    ## Generate response set
    responseSet = {}
    for questionID in data["questions"]:
        if filter == "all":
            responseSet[questionID] = data["questions"][questionID]
        elif filter == "unanswered":
            if data["questions"][questionID]["status"] == "unanswered":
                responseSet[questionID] = data["questions"][questionID]
        elif filter == "answered":
            if data["questions"][questionID]["status"] == "answered":
                responseSet[questionID] = data["questions"][questionID]
    
    ## Success
    return jsonify(responseSet)

@app.route("/api/toggleQuestionStatus", methods=['POST'])
def toggleQuestionStatus():
    global data

    ## Check headers
    if 'Content-Type' not in request.headers:
        return "ERROR: Content-Type header is not present."
    if request.headers['Content-Type'] != 'application/json':
        return "ERROR: Content-Type header is not application/json."
    if 'Key' not in request.headers:
        return "ERROR: Key header is not present."
    if request.headers['Key'] != os.environ['API_KEY']:
        return "ERROR: Key header is not valid."
    

    ## Check body
    if 'token' not in request.json:
        return "ERROR: Token not present in request body."
    if request.json['token'] != data['loggedInToken']:
        return "ERROR: Invalid token."
    if 'questionID' not in request.json:
        return "ERROR: Question ID not present in request body."
    if request.json['questionID'] not in data['questions']:
        return "ERROR: Invalid question ID."
    if 'newStatus' not in request.json:
        return "ERROR: New status not present in request body."
    if request.json['newStatus'] not in ['unanswered', 'answered']:
        return "ERROR: Invalid new status."
    
    ## Success
    data['questions'][request.json['questionID']]['status'] = request.json['newStatus']
    saveToFile(data)

    return "SUCCESS: Question status updated."