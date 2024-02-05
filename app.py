import os

from dotenv import dotenv_values, load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "user",
                "content": "Name me a different neighborhood in San Francisco",
            }
        ],
    )
    return response.choices[0].message.content
    # return render_template("index.html")


# @app.route("/palette", methods=["POST"])
# def prompt_to_pallete():
# open ai completion call
# return list of colors


if __name__ == "__main__":
    app.run(debug=True)
