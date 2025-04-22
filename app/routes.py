from flask import Blueprint, request
from app.services import process_question, save_uploaded_file

main_bp = Blueprint("main", __name__)


@main_bp.route("/question", methods=["POST"])
def answer_question():
    data = request.get_json()
    return process_question(data)


@main_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    return save_uploaded_file(file)
