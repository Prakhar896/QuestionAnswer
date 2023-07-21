const heading = document.getElementById("heading")
const questionField = document.getElementById("questionInput")
const nameField = document.getElementById("nameField")
const askButton = document.getElementById("askButton")
const mainContentDiv = document.getElementById("mainContent")

var submitted = false

function ask() {
    if (submitted) {
        location.reload()
    } else if (!questionField.value || questionField.value == "") {
        alert("Please enter a question!")
        return
    }

    var question = questionField.value
    var author = null
    if (!nameField.value || nameField.value == "") {
        author = 'Anonymous'
    } else {
        author = nameField.value
    }

    axios({
        method: 'post',
        url: `${origin}/api/askQuestion`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'question': question,
            'author': author
        }
    })
        .then(response => {
            if (response.status == 200) {
                if (!response.data.startsWith("ERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        heading.innerText = 'Your question was submitted!'
                        askButton.innerText = 'Ask Again'
                        mainContentDiv.parentElement.removeChild(mainContentDiv)
                        submitted = true
                    } else {
                        alert("Something went wrong. Please try again.")
                        console.log("Unknown response received from servers; response: " + response.data)
                    }
                } else {
                    alert("An error occurred. Please try again.")
                    console.log("Error occurred in request; response: " + response.data)
                }
            } else {
                alert("Something went wrong. Please try again.")
                console.log("Non-200 status code received from servers; response: " + response.data)
            }
        })
        .catch(error => {
            alert("An error occurred. Please try again.")
            console.log("Error in connecting to servers; error: " + error)
        })
}

questionField.addEventListener('keypress', (event) => {
    if (event.key == 'Enter') {
        ask()
    }
})
nameField.addEventListener('keypress', (event) => {
    if (event.key == 'Enter') {
        ask()
    }
})