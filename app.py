from flask import Flask, render_template
from data.dashboard_data import recent_activities

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        activities=recent_activities
    )


@app.route("/project_tracker")
def project_tracker():
    return render_template("project_tracker.html")


@app.route("/in_progress")
def in_progress():
    return render_template("in_progress.html")


@app.route("/completed_projects")
def completed_projects():
    return render_template("completed_projects.html")   


if __name__ == "__main__":
    app.run(debug=True)   

