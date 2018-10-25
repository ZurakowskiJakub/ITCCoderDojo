import os
from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import abort
from functools import reduce

app = Flask(__name__)


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def load_file(path):
    with open(path) as f:
        contents = f.read()
    return contents


@app.route('/')
def index():
    files = get_directory_structure("student_work")
    return render_template("index.html", files=files)


@app.route('/<term>/<student>/<file>')
def get_student_file(term, student, file):
    if not os.path.isfile(f"student_work/{term}/{student}/{file}"):
        abort(404)
    file_string = load_file(f"student_work/{term}/{student}/{file}")
    return render_template_string(file_string)


if __name__ == "__main__":
    app.run(debug=True)