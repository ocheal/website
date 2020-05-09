from flask import Flask, render_template, redirect, url_for
from .projects import projects

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", projects=projects)

for project in projects:
    if project.blueprint is not None:
        app.register_blueprint(project.blueprint)
