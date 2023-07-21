from main import *

@app.route("/session/<token>/unanswered")
def unansweredPage(token):
    global data

    if token != data["loggedInToken"]:
        return redirect(url_for("unauthorised"))
    
    return render_template("unanswered.html")

@app.route("/session/<token>/answered")
def answeredPage(token):
    return "WIP"