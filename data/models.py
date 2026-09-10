class RecentActivity:
    def __init__(self, id, time, text, highlight, description):
        self.id = id
        self.time = time
        self.text = text
        self.highlight = highlight
        self.description = description


class ProjectProgress:
    def __init__(self, project_id, name, progress, color):
        self.project_id = project_id
        self.name = name
        self.progress = progress
        self.color = color


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