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