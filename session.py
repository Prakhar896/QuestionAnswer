from main import *

@app.route("/session/<token>/unanswered")
def unansweredPage(token):
    global data

    if token != data["loggedInToken"]:
        return redirect(url_for("unauthorised"))
    
    return render_template("unanswered.html", token=token)

@app.route("/session/<token>/answered")
def answeredPage(token):
    global data

    if token != data["loggedInToken"]:
        return redirect(url_for("unauthorised"))
    
    return render_template("answered.html", token=token)

@app.route("/session/<token>/admin")
def adminPage(token):
    global data

    if token != data["loggedInToken"]:
        return redirect(url_for("unauthorised"))
    
    return render_template("admin.html", token=token)