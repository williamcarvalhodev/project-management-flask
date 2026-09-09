from flask import Flask, render_template
from data.dashboard_data import recent_activities, projects_progress, summary
from data.tracker_data import project_groups



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        activities=recent_activities,
        projects=projects_progress,
        summary=summary
    )


@app.route("/project_tracker")
def project_tracker():
    return render_template(
        "project_tracker.html",
        project_groups=project_groups
    )


@app.route("/in_progress")
def in_progress():
    return render_template("in_progress.html")


@app.route("/completed_projects")
def completed_projects():
    return render_template("completed_projects.html")   


if __name__ == "__main__":
    app.run(debug=True)   

