const refreshStatusButton = document.getElementById("refreshStatusButton")
const sessionStatusLabel = document.getElementById("sessionStatusLabel")
const manageStatusButton = document.getElementById("manageStatusButton")
const sessionStatusDiv = document.getElementById("sessionStatusDiv")
const numUnansweredLabel = document.getElementById("numUnansweredLabel")
const numAnsweredLabel = document.getElementById("numAnsweredLabel")
const statusLabel = document.getElementById("statusLabel")

const token = location.pathname.split("/")[2]
var sessionIsActive = manageStatusButton.innerText != "Activate"

function refreshData(fromCodeSource = false) {
    if (!fromCodeSource) {
        statusLabel.innerText = "Refreshing..."
        statusLabel.style.visibility = 'visible'
    }

    // Make request
    axios({
        method: 'post',
        url: `${origin}/api/getQuestionAnswerSessionStatus`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token
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

                        alert("Something went wrong. Please try again.")
                        console.log("Error response received in refreshing session status; response: " + response.data)
                        statusLabel.style.visibility = 'hidden'
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log("Unknown response received in refreshing session status; response: " + response.data)
                        statusLabel.style.visibility = 'hidden'
                    }
                } else {
                    var status = response.data['active']
                    sessionIsActive = status
                    if (status) {
                        status = `Active (Activated at ${response.data['activationDatetime']})`
                        manageStatusButton.innerText = 'De-activate'
                    } else {
                        status = 'Inactive'
                        manageStatusButton.innerText = 'Activate'
                    }

                    sessionStatusLabel.innerHTML = `Current Q&A Session: <strong>${status}</strong>`
                    numUnansweredLabel.innerText = `Number of unanswered questions: ${response.data['unansweredQuestions']}`
                    numAnsweredLabel.innerText = `Number of answered questions: ${response.data['answeredQuestions']}`
                    console.log("Refreshed data successfully!")
                    statusLabel.innerText = 'Refreshed successfully!'
                    statusLabel.style.visibility = 'visible'
                    setTimeout(() => {
                        statusLabel.style.visibility = 'hidden'
                    }, 1500)
                    return
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log("Non-200 status code received in refreshing session status; response: " + response.data)
                statusLabel.style.visibility = 'hidden'
            }
        })
        .catch(error => {
            alert("An error occurred in connecting to the server. Please try again.")
            console.log("Error in connecting to servers to refresh session status; error: " + error)
            statusLabel.style.visibility = 'hidden'
        })
}

function toggleSessionStatus() {
    if (sessionIsActive) {
        if (!confirm("Are you sure you want to de-activate the Q&A session? This will prevent any audience members from using the ask page to ask questions.")) { return }
    } else {
        if (!confirm("Are you sure you want to activate the Q&A session? This will allow audience members to use the ask page to ask questions.")) { return }
    }

    const newStatus = sessionIsActive ? 'inactive' : 'active'
    statusLabel.innerText = ((newStatus == 'active') ? "Activating..." : "De-activating...")
    statusLabel.style.visibility = 'visible'

    axios({
        method: 'post',
        url: `${origin}/api/toggleQuestionAnswerSession`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'newStatus': newStatus
        }
    })
    .then(response => {
        if (response.status == 200) {
            if (!response.data.startsWith("ERROR")) {
                if (!response.data.startsWith("UERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        if (newStatus == 'active') {
                            manageStatusButton.innerText = 'De-activate'
                            sessionIsActive = true
                        } else {
                            manageStatusButton.innerText = 'Activate'
                            sessionIsActive = false
                        }
                        statusLabel.innerText = 'Session status updated! Refreshing data...'
                        statusLabel.style.visibility = 'visible'
                        setTimeout(() => {
                            refreshData(fromCodeSource=true)
                        }, 800)
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log("Unknown response received from servers in updating session status; response: " + response.data)
                        statusLabel.style.visibility = 'hidden'
                    }
                } else {
                    statusLabel.innerText = response.data.substring("UERROR: ".length)
                    statusLabel.style.visibility = 'visible'
                    console.log("User error occurred in updating session status; response: " + response.data)
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log("Error response received from servers in updating session status; response: " + response.data)
                statusLabel.style.visibility = 'hidden'
            }
        } else {
            alert("Something went wrong. Please try again.")
            console.log("Non-200 status code received from servers in updating session status; response: " + response.data)
            statusLabel.style.visibility = 'hidden'
        }
    })
    .catch(error => {
        alert("An error occurred in connecting to the server. Please try again.")
        console.log("Error in connecting to servers to update session status; error: " + error)
        statusLabel.style.visibility = 'hidden'
    })
}

function deleteAll() {
    const numUnanswered = parseInt(numUnansweredLabel.innerText.substring("Number of unanswered questions: ".length))
    const numAnswered = parseInt(numAnsweredLabel.innerText.substring("Number of answered questions: ".length))
    if (numUnanswered == 0 && numAnswered == 0) {
        alert("There are no questions to delete.")
        return
    }

    if (!confirm(`Are you sure you would like to delete ALL questions?`)) {
        return
    }

    statusLabel.innerText = "Deleting all questions..."
    statusLabel.style.visibility = 'visible'

    axios({
        method: 'post',
        url: `${origin}/api/deleteQuestion`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'token': token,
            'bundleType': 'all'
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (!response.data.startsWith("ERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        statusLabel.innerText = 'All questions deleted! Refreshing data...'
                        setTimeout(() => {
                            refreshData(fromCodeSource=true)
                        }, 800)
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log(`Unknown response received from servers in deleting all questions; response: ${response.data}`)
                        statusLabel.style.visibility = 'hidden'
                    }
                } else {
                    alert("An error occurred in deleting all questions. Please try again.")
                    console.log(`Error in deleting all questions; response: ${response.data}`)
                    statusLabel.style.visibility = 'hidden'
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log(`Non-200 status code response received from server in deleting all questions; response: ${response.data}`)
                statusLabel.style.visibility = 'hidden'
            }
        })
        .catch(error => {
            alert("Failed to connect to delete all questions. Please try again.")
            console.log(`Error in connecting to servers to delete all questions; error: ${error}`)
            statusLabel.style.visibility = 'hidden'
        })
}