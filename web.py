from flask import flash, Flask, redirect, render_template, request, send_file
from event_prep import *

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        # Ensure profile was attached
        if "admiral_file" not in request.files:
            flash("Missing KC3Kai profile!")
            return redirect("/")

        admiral_file = request.files["admiral_file"]
        trimmed = admiral_file.filename.lower().strip()
        data = admiral_file.read()

        # ?
        if trimmed == "":
            flash("Missing KC3Kai profile!")
            return redirect("/")

        out = render_profile(data)

        if isinstance(out, str):
            return out

        return send_file(out, mimetype="image/png")
    except Exception as e:
        print("Exception during upload; " + str(e))
        return "Something went wrong during upload! Sorry about that :("


if __name__ == "__main__":
    app.run()
