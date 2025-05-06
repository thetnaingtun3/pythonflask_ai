import os
from openai import OpenAI


def simple_response(msg):
    return {
        "status": "success",
        "message": msg,
    }


def load_articles(data_folder):
    articles = {}
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                articles[filename] = file.read()
    return articles


def build_prompt(articles, question):
    return f"""Use the below articles to answer the subsequent question. 
If the answer cannot be found, write "I'm still learning, but I'll do my best to help with that."

Articles:
\"\"\"
{articles}
\"\"\"

Question: {question}
"""


def call_openai(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You answer questions based on given articles.",
            },
            {"role": "user", "content": prompt},
        ],
        model="gpt-4o",
        temperature=0,
    )
    return response.choices[0].message.content.strip()
