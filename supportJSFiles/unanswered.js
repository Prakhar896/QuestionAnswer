const questionsDiv = document.getElementById("questionsDiv")

const token = location.pathname.split("/")[2]
const displayType = "unanswered"
var questionData = null

function renderData() {
    if (questionData == null) {
        return
    } else if (Object.keys(questionData).length == 0) {
        questionsDiv.innerHTML = '<p>No unanswered questions at the moment.</p>'
        return
    }

    // create list
    const list = document.createElement("ul")
    for (var questionID in questionData) {
        const item = document.createElement("li")
        item.id = questionID

        const answeredButton = document.createElement('button')
        answeredButton.innerText = 'Answer'
        answeredButton.className = 'fancyButtons'
        answeredButton.onclick = questionAnswered

        item.innerHTML = `<strong>${questionData[questionID]['question']}</strong> by ${questionData[questionID]['author']} (ID: ${questionID})&nbsp;&nbsp;&nbsp;<button id="${questionID}" class="fancyButtons" onclick="questionAnswered(this)">Answer</button>`
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
    console.log(element.id)
}

fetchData()
var liveRefreshID = setInterval(() => {
    const date = new Date()
    console.log(`${date.getDate()}-${date.getMonth()+1}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()} Fetching new batch...`)
    
    fetchData()
}, 5000)

function toggleLiveRefresh() {
    if (liveRefreshID == null) {
        liveRefreshID = setInterval(() => {
            const date = new Date()
            console.log(`${date.getDate()}-${date.getMonth()+1}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()} Fetching new batch...`)
            
            fetchData()
        }, 5000)
        document.getElementById("liveRefreshToggleButton").innerText = 'Stop Live Refresh'
    } else {
        clearInterval(liveRefreshID)
        liveRefreshID = null
        document.getElementById("liveRefreshToggleButton").innerText = 'Start Live Refresh'
    }
}