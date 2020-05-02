from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

class Project:
    def __init__(self, name, href=""):
        self.name = name
        self.href = href
    
    def render_html(self):
        return f"<p>{self.name}</p>"

    def register_route(self):
        if not self.href:
            return
        @app.route(f"/{self.href}")
        def route(): #pylint: disable=unused-variable
            return render_template(f"{self.href}.html")
        
projects = [Project("boids", href="boids"),
            *[Project(f"Project #{i}") for i in range(2,8+1)]]

@app.route("/")
def index():
    return render_template("index.html", projects=projects)

@app.route("/github")
def github():
    return redirect("https://github.com/ocheal")

@app.route("/contact")
def contact():
    # return render_template("contact.html")
    return ""

for project in projects:
    project.register_route()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
