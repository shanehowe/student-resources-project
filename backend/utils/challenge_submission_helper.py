import os
from models.challenge_submissions import CodeSubmission
import requests
from requests import Response
from dotenv import load_dotenv

load_dotenv("../.env")
X_RapidAPI_Key = os.getenv("X_RapidAPI_Key")
X_RapidAPI_Host = os.getenv("X_RapidAPI_Host")


def run_submitted_code(submission: CodeSubmission) -> Response:
    url = "https://judge0-ce.p.rapidapi.com/submissions"

    querystring = {"base64_encoded":"false","fields":"*"}

    payload = {
    	"language_id": 71,
    	"source_code": submission.sourceCode,
    }
    headers = {
    	"content-type": "application/json",
    	"Content-Type": "application/json",
    	"X-RapidAPI-Key": X_RapidAPI_Key,
    	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    token = response.json()["token"]

    url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"

    querystring = {"base64_encoded":"false","fields":"stderr,stdout,status"}
    headers = {
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response