from flask import Flask, render_template, request, redirect, url_for
from data.dashboard_data import recent_activities, projects_progress, summary
from data.tracker_data import project_groups
from data.models import Project
from datetime import datetime


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


@app.route("/projects/add", methods=["POST"])
def add_project():
    group_id = int(request.form["group_id"])
    name = request.form["name"]
    client = request.form["client"]
    price = float(request.form["price"])
    designer_cost = float(request.form["designer_cost"])

    selected_group = None

    for group in project_groups:
        if group.group_id == group_id:
            selected_group = group
            break
        
    # Find the next available project ID
    project_ids = []

    for group in project_groups:
        for project in group.projects:
            project_ids.append(project.project_id)

    new_project_id = max(project_ids) + 1
    
    # Create the new project
    new_project = Project(
        project_id=new_project_id,
        name=name,
        status="Proposal Sent",
        status_class="status-proposal",
        client=client,
        price=price,
        designer_cost=designer_cost,
        start="-",
        end="-",
        days_left="Pending",
        days_left_class="project-pending",
        accepted=False
    )

    # Add the project to the selected group
    selected_group.add_project(new_project)

    return redirect(url_for("project_tracker"))


@app.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):

    # Find the project by ID and remove it from its group
    for group in project_groups:
        for project in group.projects:

            if project.project_id == project_id:
                group.delete_project(project)

                return redirect(url_for("project_tracker"))

    return redirect(url_for("project_tracker"))


@app.route("/in_progress")
def in_progress():
    in_progress_projects = []

    for group in project_groups:
        for project in group.projects:
            if project.status == "In Progress":
                in_progress_projects.append(
                    {
                        "project": project,
                        "project_type": group.name
                    }
                )

    return render_template(
        "in_progress.html",
        in_progress_projects=in_progress_projects
    )


@app.route("/completed_projects")
def completed_projects():
    completed_projects_by_month = {}

    for group in project_groups:
        for project in group.projects:

            if project.status == "Completed":
                completed_date = datetime.strptime(
                    project.end,
                    "%d/%m/%Y"
                )

                month_name = completed_date.strftime("%B %Y")

                if month_name not in completed_projects_by_month:
                    completed_projects_by_month[month_name] = []

                completed_projects_by_month[month_name].append(
                    {
                        "project": project,
                        "project_type": group.name
                    }
                )

    return render_template(
        "completed_projects.html",
        completed_projects_by_month=completed_projects_by_month
    )  


if __name__ == "__main__":
    app.run(debug=True)   

