from flask import render_template,Flask, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("layout.html")

app.config["FILE_UPLOADS"] = "/uploads"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["GLTF", "GLB", "FBX"]

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        if request.files:

            file = request.files["file"]

            if file.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config["FILE_UPLOADS"], filename))

                print("File saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("upload_file.html")

@app.route("/3d_display")
def display():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)