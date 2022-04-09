from typing import Dict

import requests


def get_categories() -> Dict[str, int]:
    resp = requests.get("https://opentdb.com/api_category.php")
    resp_json = resp.json()
    return {item["name"]: item["id"] for item in resp_json.get("trivia_categories", [])}


def get_token() -> str:
    resp = requests.get("https://opentdb.com/api_token.php?command=request").json()
    return resp.get("token")


def get_category_data(category: int, token: str):
    has_more = True
    ret = []
    while has_more:
        resp = requests.get(
            "https://opentdb.com/api.php",
            params={"category": category, "token": token, "amount": 10},
        )
        has_more = False
        resp_json = resp.json()
        if resp_json.get("response_code") == 0 and resp_json.get("results"):
            has_more = True
            ret += resp_json.get("results")
    return ret
