from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from database.database import database
from models.challenge_submissions import ChallengeDocument, CodeSubmission
import os
from utils.challenge_submission_helper import run_submitted_code
from utils.JWTHelper import JwtHelper


challlenge_router = APIRouter()

@challlenge_router.post("/api/challenges/code-submission", response_model=None)
def submit_code(submission: CodeSubmission, request: Request):
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )
    
    # Will raise a HTTP exception if it cant decode the token
    JwtHelper.decode_token(token[7:])
    
    if "print" in submission.sourceCode:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No print statement allowed in source code."
        )
    
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(
        os.path.join(basepath, "..", "code_submission_tests", f"{submission.functionName}.py")
        )

    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            code = "".join(lines)
            code += f"\nprint(test({submission.functionName}))"
            submission.sourceCode += f"\n{code}"
    except FileNotFoundError:
        return JSONResponse(
            content="Error Function Name must not be modified",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    response = run_submitted_code(submission)

    json_response: dict = response.json()
    try:      
        if "^\nIndentationError:" in json_response.get("stderr"):
            json_response["stderr"] = "Error:\nIndentationError,\nCheck your code is indented properly."
        elif "File too large" in json_response.get("stderr"):
            json_response["stderr"] = "Maximum stdout limit.\nYou likely have an infinite loop."
    except TypeError:
        pass

    return {"data": json_response}


@challlenge_router.get("/api/challenges", response_model=None)
def get_all_challenges() -> list[ChallengeDocument]:
    challenge_coll = database.db.pythonChallenges
    return [ChallengeDocument(**challenge) for challenge in challenge_coll.find()]
