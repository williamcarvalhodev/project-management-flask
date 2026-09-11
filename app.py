from flask import Flask, render_template, request, redirect, url_for
from data.dashboard_data import recent_activities, summary
from data.tracker_data import project_groups
from data.models import Project
from datetime import datetime


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    projects_progress = []
    pending_approval = 0
    completed_tasks = 0

    # Get projects currently in progress and pending approval
    for group in project_groups:
        for project in group.projects:

            if project.status == "In Progress":
                projects_progress.append(project)
                completed_tasks += project.completed_tasks

            if project.status == "Proposal Sent":
                pending_approval += 1

    # Order projects from highest to lowest progress
    projects_progress.sort(
        key=Project.calculate_progress,
        reverse=True
    )

    monthly_earnings = 0
    annual_earnings = 0
    current_date = datetime.now()

    # Calculate monthly and annual earnings
    for group in project_groups:
        for project in group.projects:

            if project.status == "Completed":

                completed_date = project.get_completed_date()

                # Monthly earnings
                if (
                    completed_date.month == current_date.month
                    and completed_date.year == current_date.year
                ):
                    monthly_earnings += project.calculate_net()

                # Annual earnings
                if completed_date.year == current_date.year:
                    annual_earnings += project.calculate_net()

    # Update dashboard summary
    summary["monthly_earnings"].value = f"€{monthly_earnings:,.0f}"
    summary["annual_earnings"].value = f"€{annual_earnings:,.0f}"
    summary["pending_approval"].value = pending_approval
    summary["task_completion"].value = completed_tasks

    return render_template(
        "dashboard.html",
        activities=recent_activities,
        projects=projects_progress,
        summary=summary
    )


@app.route("/project_tracker")
def project_tracker():

    # Update days left for active projects
    for group in project_groups:
        for project in group.projects:

            if project.status == "In Progress":
                project.update_days_left()

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


@app.route("/projects/<int:project_id>/start", methods=["POST"])
def start_project(project_id):
    start_date = request.form["start"]
    end_date = request.form["end"]

    # Convert dates to dd/mm/yyyy
    start_date = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    end_date = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    # Find the project and start it
    for group in project_groups:
        for project in group.projects:

            if project.project_id == project_id:

                project.start_project(
                    start_date,
                    end_date,
                    group.get_total_tasks()
                )

                return redirect(url_for("project_tracker"))

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

    # Order projects by closest deadline
    in_progress_projects.sort(
        key=lambda item: datetime.strptime(
            item["project"].end,
            "%d/%m/%Y"
        )
    )

    return render_template(
        "in_progress.html",
        in_progress_projects=in_progress_projects
    )
    
    
@app.route("/projects/<int:project_id>/complete", methods=["POST"])
def complete_project(project_id):

    invoice_required = request.form["invoice_required"]
    project_link = request.form["project_link"]

    # Find the project by ID and mark it as completed
    for group in project_groups:
        for project in group.projects:

            if project.project_id == project_id:

                # Only complete projects with all tasks finished
                if project.calculate_progress() < 100:
                    return redirect(url_for("in_progress"))

                project.invoice_required = invoice_required == "yes"
                project.project_link = project_link

                project.status = "Completed"
                project.status_class = "status-completed"

                project.days_left = "Completed"
                project.days_left_class = "project-completed"

                project.completed_date = datetime.now().strftime(
                    "%d/%m/%Y"
                )

                return redirect(url_for("completed_projects"))

    return redirect(url_for("in_progress"))


@app.route("/completed_projects")
def completed_projects():
    completed_projects_by_month = {}

    for group in project_groups:
        for project in group.projects:

            if project.status == "Completed":

                completed_date = project.get_completed_date()

                month_name = completed_date.strftime("%B %Y")

                if month_name not in completed_projects_by_month:
                    completed_projects_by_month[month_name] = {
                        "projects": [],
                        "total_net": 0
                    }

                completed_projects_by_month[month_name]["projects"].append(
                    {
                        "project": project,
                        "project_type": group.name
                    }
                )

                completed_projects_by_month[month_name]["total_net"] += project.calculate_net()

    # Order months from newest to oldest
    completed_projects_by_month = dict(
        sorted(
            completed_projects_by_month.items(),
            key=lambda item: datetime.strptime(
                item[0],
                "%B %Y"
            ),
            reverse=True
        )
    )

    return render_template(
        "completed_projects.html",
        completed_projects_by_month=completed_projects_by_month
    )


if __name__ == "__main__":
    app.run(debug=True)   

