from flask import Flask
import dotenv
import openai
import os

dotenv.load_dotenv()

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("OPENAI_API_KEY is not set")

PORT = int(os.getenv("APP_PORT", 8080))


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
