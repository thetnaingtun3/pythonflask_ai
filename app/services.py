import os
from flask import jsonify
from app.utils import load_articles, build_prompt, call_openai

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
        return jsonify(
            {
                "status": "success",
                "message": "Answer generated successfully",
                "answer": answer,
                
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "answer": None}), 500


def save_uploaded_file(file):
    if not file:
        return (
            jsonify({"status": "error", "message": "No file part in the request"}),
            400,
        )

    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected"}), 400

    if not file.filename.endswith(".txt"):
        return (
            jsonify({"status": "error", "message": "Only .txt files are allowed"}),
            400,
        )

    try:
        file_path = os.path.join(data_folder, file.filename)
        file.save(file_path)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"File '{file.filename}' uploaded successfully",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
