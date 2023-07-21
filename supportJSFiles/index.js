const passwordField = document.getElementById("passwordField")
const statusLabel = document.getElementById("statusLabel")

function login() {
    if (!passwordField.value || passwordField.value == "") {
        alert("Please enter your admin password.")
        return
    }

    const pass = passwordField.value
    statusLabel.innerText = 'Processing...'
    statusLabel.style.visibility = 'visible'

    axios({
        method: 'post',
        url: `${origin}/api/login`,
        headers: {
            'Content-Type': 'application/json',
            'Key': "\{{ API_KEY }}"
        },
        data: {
            'pass': pass
        }
    })
    .then(response => {
        if (response.status == 200) {
            if (!response.data.startsWith("ERROR")) {
                if (!response.data.startsWith("UERROR")) {
                    if (response.data.startsWith("SUCCESS")) {
                        statusLabel.innerText = 'Logged in! Redirecting now...'

                        const loggedInToken = response.data.substring("SUCCESS: Logged in; Token: ".length)

                        location.href = `/session/${loggedInToken}/unanswered`
                    } else {
                        alert("Unknown response received from server. Please try again.")
                        console.log("Unknown response received; response: " + response.data)
                        statusLabel.style.visibility = 'hidden'
                    }
                } else {
                    statusLabel.innerText = response.data.substring("UERROR: ".length)
                    console.log("User error occurred; response: " + response.data)
                }
            } else {
                alert("An error occurred. Please try again.")
                console.log("Error occurred in logging in; response: " + response.data)
                statusLabel.style.visibility = 'hidden'
            }
        } else {
            alert("An error occurred. Please try again.")
            console.log("Received non-200 status code response; response: " + response.data)
            statusLabel.style.visibility = 'hidden'
        }
    })
    .catch(error => {
        alert("Failed to connect to servers. Please try again.")
        console.log("Error occurred in connecting to server; error: " + error)
        statusLabel.style.visibility = 'hidden'
    })
}

passwordField.addEventListener('keypress', event => {
    if (event.key == 'Enter') {
        login()
    }
})