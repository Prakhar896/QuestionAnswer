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
    for questionID in copy.deepcopy(data["questions"]):
        if filter == "all":
            responseSet[questionID] = copy.deepcopy(data["questions"][questionID])
        elif filter == "unanswered":
            if data["questions"][questionID]["status"] == "unanswered":
                responseSet[questionID] = copy.deepcopy(data["questions"][questionID])
        elif filter == "answered":
            if data["questions"][questionID]["status"] == "answered":
                responseSet[questionID] = copy.deepcopy(data["questions"][questionID])
    
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

@app.route("/api/askQuestion", methods=['POST'])
def askQuestion():
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
    if 'question' not in request.json:
        return "ERROR: Question not present in request body."
    if 'author' not in request.json:
        return "ERROR: Author not present in request body."
    
    ## Logic checks
    if not data["session"]["active"]:
        return "UERROR: The admin has not activated the Q&A session yet."
    
    ## Success
    questionID = generateQuestionID(thatIsNotIn=[x for x in data['questions']])
    data['questions'][questionID] = {
        'question': request.json['question'],
        'author': request.json['author'],
        'status': 'unanswered'
    }
    saveToFile(data)

    return "SUCCESS: Question added."

@app.route('/api/deleteQuestion', methods=['POST'])
def deleteQuestion():
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
        if 'bundleType' not in request.json:
            return "ERROR: Invalid question/question bundle identifiers provided for deletion."
        if request.json['bundleType'] not in ['all', 'unanswered', 'answered']:
            return "ERROR: Invalid question bundle type."
    elif request.json['questionID'] not in data['questions']:
        return "ERROR: Invalid question ID."
    
    ## Success
    if 'questionID' in request.json:
        del data['questions'][request.json['questionID']]
    else:
        if request.json['bundleType'] == 'all':
            data['questions'] = {}
        elif request.json['bundleType'] == 'unanswered':
            for questionID in copy.deepcopy(data['questions']):
                if data['questions'][questionID]['status'] == 'unanswered':
                    del data['questions'][questionID]
        elif request.json['bundleType'] == 'answered':
            for questionID in copy.deepcopy(data['questions']):
                if data['questions'][questionID]['status'] == 'answered':
                    del data['questions'][questionID]

    saveToFile(data)

    return "SUCCESS: Question or question bundle deleted."

@app.route("/api/toggleQuestionAnswerSession", methods=['POST'])
def toggleQuestionAnswerSession():
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
    if "newStatus" not in request.json:
        return "ERROR: New status not present in request body."
    if request.json["newStatus"] not in ["active", "inactive"]:
        return "ERROR: Invalid new status."
    if request.json["newStatus"] == "active" and data["session"]["active"]:
        return "UERROR: Session is already active. Please refresh."
    if request.json["newStatus"] == "inactive" and not data["session"]["active"]:
        return "UERROR: Session is already inactive. Please refresh."
    
    ## Success
    newStatus = request.json["newStatus"] == "active"
    data["session"]["active"] = newStatus
    if newStatus:
        data["session"]["activationDatetime"] = datetime.datetime.now().strftime(Universal.datetimeFormat)
    saveToFile(data)

    return "SUCCESS: Q&A session status updated."

@app.route("/api/getQuestionAnswerSessionStatus", methods=['POST'])
def getQuestionAnswerSessionStatus():
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
    
    ## Success
    response = copy.deepcopy(data['session'])
    response['activationDatetime'] = Universal.generateReadableDatetime(response['activationDatetime'])
    response['unansweredQuestions'] = len([x for x in data['questions'] if data['questions'][x]['status'] == 'unanswered'])
    response['answeredQuestions'] = len([x for x in data['questions'] if data['questions'][x]['status'] == 'answered'])
    return jsonify(response)