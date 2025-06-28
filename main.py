from typing import Dict
from flask import Flask, request
from flask_cors import CORS
import requests
import dotenv
import openai
import os

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://political-engagement-app.vercel.app"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("OPENAI_API_KEY is not set")
if CONGRESS_API_KEY is None:
    raise Exception("CONGRESS_API_KEY is not set")
LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if LEGISCAN_API_KEY is None:
    raise Exception("LEGISCAN_API_KEY is not set")

CONGRESS_API_URL = "https://api.congress.gov/v3/"
LEGISCAN_API_URL = f"https://api.legiscan.com/?key={LEGISCAN_API_KEY}&op=getSearch"  # &state=STATE&query=QUERY"


PORT = int(os.getenv("APP_PORT", 8080))
DEBUG = os.getenv("APP_DEBUG", False) == "true"


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/search", methods=["GET"])
def search():
    params = request.args
    state = params["state"]
    query = params["query"]
    url = f"{LEGISCAN_API_URL}&state={state}&query={query}"
    response = requests.get(url)
    data = response.json()["searchresult"]
    # create a new list of objects that only has "bill_id", "bill_number", "title"
    ret_data = []
    count = int(data["summary"]["range"].split()[-1])
    for i in range(1, count):
        datum = data[str(i)]
        ret_data.append(
            {
                "bill_id": datum["bill_id"],
                "bill_number": datum["bill_number"],
                "title": datum["title"],
            }
        )
    return ret_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
