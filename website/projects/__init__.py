class Project:
    def __init__(self, name, href="", blueprint=None):
        self.name = name
        self.href = href
        self.blueprint = blueprint
    
    def render_html(self):
        center = "position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%)"
        return f"<p style='{center}'>{self.name}</p>"

projects = []
from .boids import boids
projects.append(boids)

for i in range(2,4+1):
    projects.append(Project(f"Project #{i}"))
