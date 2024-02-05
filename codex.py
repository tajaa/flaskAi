import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

PROMPT = """
        You will receive a files content as text. Generate a code review for the file. Indicate what changes should be made to improve its style, performance and maintainability. If there are reputable libraries that could be introduced to improve the code, suggest them. Be kind and constructive. For each suggested change, include line numbers to which you are referring but also show me the code altogether so taht I can easily copy and paste. Please annotate where you've changed, removed, or modified something'
    """


def code_review(file_path, model):
    with open(file_path, "r") as file:
        content = file.read()
        generated_code_review = make_review_request(content, model)
        print(generated_code_review)


def make_review_request(filecontent, model):
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"Code reivew the following file: {filecontent}"},
    ]
    res = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
    )
    return res.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Simple code reviewer")
    parser.add_argument("file")
    parser.add_argument("--model", default="gpt-4-turbo-preview")
    args = parser.parse_args()
    code_review(args.file, args.model)


if __name__ == "__main__":
    main()
