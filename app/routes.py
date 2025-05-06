from flask import Blueprint, request, jsonify
from app.services import process_question, save_uploaded_file, get_db_connection
from app.utils import simple_response


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    hell = "home"
    return simple_response(hell)


@main_bp.route("/question", methods=["POST"])
def answer_question():
    data = request.get_json()
    return process_question(data)


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    return save_uploaded_file(file)


# Testing route hello print
@main_bp.route("/hello", methods=["GET"])
def hello():
    return "Hello, Universe!"


@main_bp.route("/users", methods=["GET"])
def index():

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
