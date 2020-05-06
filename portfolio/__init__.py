def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", action="store_true",
                        help="run server from frozen files")
    parser.add_argument("--build", action="store_true",
                        help="build frozen files without hosting a server")
    args = parser.parse_args()
    if (args.build and args.frozen):
        raise ValueError("Mututally exclusive options build and frozen can't both be set")
    return parser.parse_args()

from flask import Flask, render_template, redirect, url_for
from projects import projects # TODO: set this up as a proper module

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", projects=projects)

for project in projects:
    if project.blueprint is not None:
        app.register_blueprint(project.blueprint)

if __name__ == "__main__":
    import sys
    args = parse_args()
    if args.build or args.frozen:
        from flask_frozen import Freezer
        freezer = Freezer(app)
        if args.build:
            freezer.freeze()
        else:
            freezer.run(port=5000, debug=True)
    else:
        app.run(port=5000, debug=True)
