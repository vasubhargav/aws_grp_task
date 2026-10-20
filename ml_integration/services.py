
import os
import requests

ML_API_BASE_URL = os.getenv(
    "ML_API_BASE_URL",
    "https://aws-grp-task-2.onrender.com"
)


def call_ml_model(endpoint, payload):
    url = f"{ML_API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    response = requests.post(
        url,
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    return response.json()
