import os
import json
from flask import jsonify, Response
from app.utils import load_articles, build_prompt, call_openai

# import mysql.connector


from dotenv import load_dotenv

load_dotenv()
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

articles = load_articles(data_folder)


def process_question(data):
    user_question = data.get("question", "")
    if not user_question:
        return (
            jsonify(
                {"status": "error", "message": "Question not provided", "answer": None}
            ),
            400,
        )

    combined_articles = "\n\n".join(articles.values())
    prompt = build_prompt(combined_articles, user_question)

    try:
        answer = call_openai(prompt)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Answer generated successfully",
                    "answer": answer,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "answer": None}), 500


def save_uploaded_file(file):
    if not file:
        response = {"status": "error", "message": "No file part in the request"}
        return Response(
            json.dumps(response, indent=4), status=400, mimetype="application/json"
        )

    if file.filename == "":
        response = {"status": "error", "message": "No file selected"}
        return Response(
            json.dumps(response, indent=4), status=400, mimetype="application/json"
        )

    if not file.filename.endswith(".txt"):
        response = {"status": "error", "message": "Only .txt files are allowed"}
        return Response(
            json.dumps(response, indent=4), status=400, mimetype="application/json"
        )

    try:
        file_path = os.path.join(data_folder, file.filename)
        file.save(file_path)
        response = {
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully",
        }
        return Response(
            json.dumps(response, indent=4), status=200, mimetype="application/json"
        )
    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return Response(
            json.dumps(response, indent=4), status=500, mimetype="application/json"
        )


# def get_db_connection():
#     connection = mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME"),
#     )
#     return connection
