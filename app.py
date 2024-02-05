import json
import os

from dotenv import dotenv_values, load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


app = Flask(__name__, template_folder="templates")


def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistnat that responds to text prompts for color pallets. You should generate color palettes that fit the theme, mood or isntructions in the prompt. The palettes should be betwen 2 and 8 colors.

    Q: convert the following verbal description of a color palete into a list of colros: The Mediterrenean Sea 
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]

    Desired format: A JSON array of hexadecimal color codes

    A: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
    )
    colors = json.loads(response.choices[0].message.content)
    return {"colors": colors}


# @app.route("/")
# def index():
#    response = client.chat.completions.create(
#        model="gpt-3.5-turbo-0125",
#        messages=[
#            {
#                "role": "user",
#                "content": "Name me a different neighborhood in San Francisco",
#            }
#        ],
#    )
# return response.choices[0].message.content
# return render_template("index.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/palette", methods=["POST"])
def prompt_to_pallete():
    # app.logger.info("HIT THE POST REQUEST ROUTE")
    # app.logger.info(request.form.get("query"))
    query = request.form.get("query")
    colors = get_colors(query)
    return colors


# open ai completion call
# return list of colors


if __name__ == "__main__":
    app.run(debug=True)
