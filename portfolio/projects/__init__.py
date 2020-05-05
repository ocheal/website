class Project:
    def __init__(self, name, href="", blueprint=None):
        self.name = name
        self.href = href
        self.blueprint = blueprint
    
    def render_html(self):
        return f"<p>{self.name}</p>"

projects = []
from .boids import boids
projects.append(boids)

for i in range(2,8+1):
    projects.append(Project(f"Project #{i}"))

