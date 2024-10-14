import json
import logging


from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend import distance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(distance.router)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    if request.method == "POST":
        try:
            # Read the JSON payload of the POST request
            request_body = await request.json()
        except json.JSONDecodeError:
            # Handle JSON decoding error if needed
            request_body = None

        logging.info(
            f"Received POST request: {request.method} {request.url}",
            extra={"data": request_body},
        )

    response: Response = await call_next(request)

    return response


@app.on_event("startup")
def startup():
    log_data = {
        "level": "%(levelname)s",
        "time": "%(asctime)s",
        "message": "%(message)s",
        "data": "%(data)s",
    }
    json_string = json.dumps(log_data)

    logging.basicConfig(
        level=logging.INFO,
        format=json_string,
        handlers=[logging.StreamHandler()],
    )


@app.get("/")
def main():
    return HTMLResponse("This is carrier-calculator backend. Make post query to /fee")
