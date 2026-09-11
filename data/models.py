from datetime import datetime

class RecentActivity:
    def __init__(self, id, time, text, highlight, description):
        self.id = id
        self.time = time
        self.text = text
        self.highlight = highlight
        self.description = description


class SummaryCard:
    def __init__(self, id, category, value, url):
        self.id = id
        self.category = category
        self.value = value
        self.url = url


class Project:
    def __init__(
        self,
        project_id,
        name,
        status,
        status_class,
        client,
        price,
        designer_cost,
        start,
        end,
        days_left,
        days_left_class,
        accepted=False,
        total_tasks=0,
        completed_tasks=0,
        invoice_required=False,
        project_link="", 
        completed_date=None       
    ):
        self.project_id = project_id
        self.name = name
        self.status = status
        self.status_class = status_class
        self.client = client
        self.price = price
        self.designer_cost = designer_cost
        self.start = start
        self.end = end
        self.days_left = days_left
        self.days_left_class = days_left_class
        self.accepted = accepted
        self.total_tasks = total_tasks
        self.completed_tasks = completed_tasks
        self.invoice_required = invoice_required
        self.project_link = project_link
        self.completed_date = completed_date

    def calculate_net(self):
        if not self.accepted:
            return 0

        return self.price - self.designer_cost
    
    # Calculate project progress based on completed tasks
    def calculate_progress(self):
        if self.total_tasks == 0:
            return 0

        return int(
            (self.completed_tasks / self.total_tasks) * 100
        )
        
    # Get project completion date
    def get_completed_date(self):
        date_value = self.completed_date or self.end

        return datetime.strptime(
            date_value,
            "%d/%m/%Y"
        )
        
    # Update days left based on project end date
    def update_days_left(self):
        current_date = datetime.now().date()

        end_date = datetime.strptime(
            self.end,
            "%d/%m/%Y"
        ).date()

        days_left = (end_date - current_date).days

        if days_left > 0:
            self.days_left = f"{days_left} days"
        elif days_left == 0:
            self.days_left = "Today"
        else:
            self.days_left = "Overdue"
            
    # Start the project
    def start_project(self, start_date, end_date, total_tasks):
        self.start = start_date
        self.end = end_date
        self.status = "In Progress"
        self.status_class = "status-in-progress"
        self.accepted = True
        self.total_tasks = total_tasks
        self.completed_tasks = 0        


class ProjectGroup:
    def __init__(self, group_id, name, projects):
        self.group_id = group_id    
        self.name = name
        self.projects = projects

    def project_count(self):
        return len(self.projects)

    def total_net(self):
        return sum(
            project.calculate_net()
            for project in self.projects
        )

    def add_project(self, project):
        self.projects.append(project)

    def delete_project(self, project):
        self.projects.remove(project)
        
    # Get total tasks based on project category
    def get_total_tasks(self):
        if self.name == "E-commerce Websites":
            return 23

        elif self.name == "Landing Pages":
            return 18

        elif self.name == "Institutional Websites":
            return 16

        return 0    

    # Order projects by status
    def ordered_projects(self):
        ordered_projects = []

        status_order = [
            "Proposal Sent",
            "In Progress",
            "Completed"
        ]

        for status in status_order:
            for project in self.projects:
                if project.status == status:
                    ordered_projects.append(project)

        return ordered_projects   