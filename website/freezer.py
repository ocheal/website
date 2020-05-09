from flask_frozen import Freezer

from . import app

freezer = Freezer(app)
app.config["FREEZER_DESTINATION"] = "../../ocheal.github.io"
app.config["FREEZER_DESTINATION_IGNORE"] = [".git*"]
