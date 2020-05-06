from flask import Blueprint, render_template

blueprint = Blueprint("boids", __name__,
                      static_folder="static",
                      template_folder="templates",
                      static_url_path="/projects/boids")

@blueprint.route("/boids/")
def route():
    return render_template(f"boids.html")

from .. import Project
boids = Project("boids", href="/boids/", blueprint=blueprint)
