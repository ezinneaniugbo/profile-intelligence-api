import requests
from rest_framework import status
from rest_framework.exceptions import APIException

GENDERIZE_URL = "https://api.genderize.io"
AGIFY_URL = "https://api.agify.io"
NATIONALIZE_URL = "https://api.nationalize.io"


class ExternalAPIException(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY

    def __init__(self, api_name="ExternalAPI", detail=None):
        self.api_name = api_name
        self.detail = detail or f"{api_name} returned an invalid response"

def fetch_gender(name: str):
    try:
        resp = requests.get(GENDERIZE_URL, params={"name": name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        raise ExternalAPIException("Genderize")

    if data.get("gender") is None or data.get("count", 0) == 0:
        raise ExternalAPIException("Genderize")

    return {
        "gender": data["gender"],
        "gender_probability": data["probability"],
        "sample_size": data["count"],
    }


def fetch_age(name: str):
    try:
        resp = requests.get(AGIFY_URL, params={"name": name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        raise ExternalAPIException("Agify")

    if data.get("age") is None:
        raise ExternalAPIException("Agify")

    age = data["age"]

    if 0 <= age <= 12:
        age_group = "child"
    elif 13 <= age <= 19:
        age_group = "teenager"
    elif 20 <= age <= 59:
        age_group = "adult"
    else:
        age_group = "senior"

    return {
        "age": age,
        "age_group": age_group,
    }


def fetch_nationality(name: str):
    try:
        resp = requests.get(NATIONALIZE_URL, params={"name": name}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        raise ExternalAPIException("Nationalize")

    country_list = data.get("country", [])

    if not country_list:
        raise ExternalAPIException("Nationalize")

    best = max(country_list, key=lambda x: x["probability"])

    return {
        "country_id": best["country_id"],
        "country_probability": best["probability"],
    }


def get_name_data(name: str):
    gender_info = fetch_gender(name)
    age_info = fetch_age(name)
    country_info = fetch_nationality(name)

    return {
        **gender_info,
        **age_info,
        **country_info,
    }