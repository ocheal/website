from flask import Flask, render_template, redirect, url_for
from projects import projects # TODO: set this up as a proper module

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", projects=projects)

@app.route("/github/")
def github():
    return render_template("index.html", projects=projects) #return redirect("https://github.com/ocheal")

@app.route("/contact/")
def contact():
    # return render_template("contact.html")
    return ""

for project in projects:
    if project.blueprint is not None:
        app.register_blueprint(project.blueprint)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        from flask_frozen import Freezer
        freezer = Freezer(app)
        # freezer.freeze()
        freezer.run(port=5000, debug=True)
    else:
        app.run(port=5000, debug=True)
