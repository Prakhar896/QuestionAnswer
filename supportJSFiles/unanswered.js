const questionsDiv = document.getElementById("questionsDiv")

const token = location.pathname.split("/")[2]
const displayType = "unanswered"
var questionData = null

function renderData() {
    if (questionData == null) {
        return
    } else if (Object.keys(questionData).length == 0) {
        questionsDiv.innerHTML = '<p id="noQuestions">No unanswered questions at the moment.</p>'
        return
    }

    // create list
    const list = document.createElement("ul")
    for (var questionID in questionData) {
        const item = document.createElement("li")
        item.id = questionID
        const answerButtonHTML = `<button id="answer${questionID}" class="fancyButtons" onclick="questionAnswered(this)">Answer</button>`
        const deleteButtonHTML = `<button id="delete${questionID}" class="fancyButtons" onclick="deleteQuestion(this)">Delete</button>`
        item.innerHTML = `<strong>${questionData[questionID]['question']}</strong> by ${questionData[questionID]['author']} (ID: ${questionID})&nbsp;&nbsp;&nbsp;${answerButtonHTML}&nbsp;&nbsp;&nbsp;${deleteButtonHTML}`
        list.appendChild(item)
    }

    questionsDiv.innerHTML = list.outerHTML
}

function fetchData() {
    axios({
        method: 'post',
        url: `${origin}/api/requestQuestionData`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'filter': displayType
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (typeof response.data == 'string') {
                    if (response.data.startsWith("ERROR")) {
                        if (response.data == "ERROR: Invalid token.") {
                            alert("Your authentication token seems to be invalid. You will be re-directed for re-login.")
                            location.href = origin
                            return
                        }

                        alert("An error occurred in fetching question data. Please try again.")
                        console.log("Error response received; response: " + response.data)
                    } else {
                        alert("An unknown response was received from the server. Please try again.")
                        console.log("Unknown response received from server; response: " + response.data)
                    }
                } else {
                    // Success case
                    questionData = response.data
                    renderData()
                }
            } else {
                alert("Unknown response received from server. Please try again.")
                console.log("Non-200 status code response received; response: " + response.data)
            }
        })
        .catch(error => {
            alert("Failed to connect to server. Please try again.")
            console.log("Error in connecting to server; error: " + error)
        })
}

function questionAnswered(element) {
    axios({
        method: 'post',
        url: `${origin}/api/toggleQuestionStatus`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'questionID': element.id.substring("answer".length),
            'newStatus': 'answered'
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (!response.data.startsWith("ERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        alert("Question marked as answered!")
                        fetchData()
                    } else {
                        alert("Unknown response received from server. Please try again.")
                        console.log("Unknown response received; response: " + response.data)
                    }
                } else {
                    alert("An error occurred. Please try again.")
                    console.log("Error occurred in marking as answered; response: " + response.data)
                }
            } else {
                alert("An error occurred. Please try again.")
                console.log("Received non-200 status code response; response: " + response.data)
            }
        })
        .catch(error => {
            alert("Failed to connect to servers. Please try again.")
            console.log("Error occurred in connecting to server; error: " + error)
        })
}

function deleteQuestion(element) {
    const questionID = element.id.substring("delete".length)
    if (!confirm(`Are you sure you would like to delete the question with ID ${questionID}?`)) {
        return
    }

    axios({
        method: 'post',
        url: `${origin}/api/deleteQuestion`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'questionID': questionID
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (!response.data.startsWith("ERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        alert("Question deleted!")
                        fetchData()
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log(`Unknown response received from servers in deleting question with ID ${questionID}; response: ${response.data}`)
                    }
                } else {
                    alert("An error occurred in deleting the question. Please try again.")
                    console.log(`Error in deleting question with ID ${questionID}; response: ${response.data}`)
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log(`Non-200 status code response received from server in deleting question with ID ${questionID}; response: ${response.data}`)
            }
        })
        .catch(error => {
            alert("Failed to connect to delete the question. Please try again.")
            console.log(`Error in connecting to servers to delete question with ID ${questionID}; error: ${error}`)
        })
}

function deleteAll() {
    if (Object.keys(questionData).length == 0) {
        alert("There are no unanswered questions to delete.")
        return
    }

    axios({
        method: 'post',
        url: `${origin}/api/deleteQuestion`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'bundleType': displayType
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (!response.data.startsWith("ERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        alert("All unanswered questions deleted!")
                        fetchData()
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log(`Unknown response received from servers in deleting all unanswered questions; response: ${response.data}`)
                    }
                } else {
                    alert("An error occurred in deleting all unanswered questions. Please try again.")
                    console.log(`Error in deleting all unanswered questions; response: ${response.data}`)
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log(`Non-200 status code response received from server in deleting all unanswered questions; response: ${response.data}`)
            }
        })
        .catch(error => {
            alert("Failed to connect to delete all unanswered questions. Please try again.")
            console.log(`Error in connecting to servers to delete all unanswered questions; error: ${error}`)
        })
}

function refresh() {
    const date = new Date()
    console.log(`${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()} Fetching new batch...`)

    fetchData()
}

fetchData()
var liveRefreshID = setInterval(refresh, 3000)

function toggleLiveRefresh() {
    if (liveRefreshID == null) {
        liveRefreshID = setInterval(refresh, 3000)
        document.getElementById("liveRefreshToggleButton").innerText = 'Stop Live Refresh'
    } else {
        clearInterval(liveRefreshID)
        liveRefreshID = null
        document.getElementById("liveRefreshToggleButton").innerText = 'Start Live Refresh'
    }
}