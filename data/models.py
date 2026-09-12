from datetime import datetime

class RecentActivity:
    def __init__(self, id, time, text, highlight, description):
        self.id = id
        self.time = time
        self.text = text
        self.highlight = highlight
        self.description = description


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
        completed_date=None,
        tasks=None       
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
        self.tasks = tasks if tasks is not None else []

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
    def start_project(self, start_date, end_date, task_names):
        self.start = start_date
        self.end = end_date
        self.status = "In Progress"
        self.status_class = "status-in-progress"
        self.accepted = True
        self.total_tasks = len(task_names)
        self.completed_tasks = 0
        self.create_tasks(task_names)
        
    # Complete the project
    def complete_project(self, invoice_required, project_link, completed_date):
        self.invoice_required = invoice_required
        self.project_link = project_link
        self.status = "Completed"
        self.status_class = "status-completed"
        self.days_left = "Completed"
        self.days_left_class = "project-completed"
        self.completed_date = completed_date
        
    # Create project tasks
    def create_tasks(self, task_names):
        self.tasks = []

        for task_id, task_name in enumerate(task_names, start=1):
            task = Task(
                task_id=task_id,
                name=task_name
            )

            self.tasks.append(task) 
            
    # Update completed tasks
    def update_completed_tasks(self):
        completed_tasks = 0

        for task in self.tasks:
            if task.completed:
                completed_tasks += 1

        self.completed_tasks = completed_tasks                      


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

    # Get tasks based on project category
    def get_task_names(self):
        if self.name == "E-commerce Websites":
            return [
                "Planning & Layout Definition",
                "Design System",
                "Design Header/Footer",
                "Create Header/Footer",
                "Build Filter System",
                "Create Test Products",
                "Design Product Layout",
                "Develop Product Layout",
                "Design Home Page",
                "Develop Home Page",
                "Design About Page",
                "Develop About Page",
                "Design Shop Page",
                "Develop Shop Page",
                "Design Contact Page",
                "Develop Contact Page",
                "Create Checkout Page",
                "Customize WooCommerce Email Templates",
                "Test Full Purchase Flow",
                "Test Emails",
                "Configure Hosting Environment",
                "Integrate Payment Gateways",
                "Website Publishing"
            ]

        elif self.name == "Landing Pages":
            return [
                "Planning & Layout Definition",
                "Design System",
                "Design Header/Footer",
                "Create Header/Footer",
                "Design Hero Section",
                "Develop Hero Section",
                "Design Benefits Section",
                "Develop Benefits Section",
                "Design Services Section",
                "Develop Services Section",
                "Design Testimonials Section",
                "Develop Testimonials Section",
                "Design Contact Form",
                "Develop Contact Form",
                "Responsive Adjustments",
                "SEO Setup",
                "Performance Testing",
                "Website Publishing"
            ]

        elif self.name == "Institutional Websites":
            return [
                "Planning & Layout Definition",
                "Design System",
                "Design Header/Footer",
                "Create Header/Footer",
                "Design Home Page",
                "Develop Home Page",
                "Design About Page",
                "Develop About Page",
                "Design Services Page",
                "Develop Services Page",
                "Design Contact Page",
                "Develop Contact Page",
                "Responsive Adjustments",
                "SEO Setup",
                "Performance Testing",
                "Website Publishing"
            ]

        return []

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
    
    
class Task:
    def __init__(self, task_id, name, completed=False):
        self.task_id = task_id
        self.name = name
        self.completed = completed
        
    # Get task owner based on task type
    def get_owner(self):
        if "Design" in self.name:
            return "Designer"

        return "Developer"
    
    # Toggle task completion
    def toggle_completed(self):
        self.completed = not self.completed        