import datetime
import json

import urllib
from typing import Dict

import requests
import slugify
import config

headers = {
    "Authorization": f"Bearer {config.transifex_token}",
    "Content-Type": "application/vnd.api+json",
}


def generate_resource_slug(category_id: int, category_name: str) -> str:
    return f"{slugify.slugify(category_name)}_{category_id}"


def create_resource(resource_slug: str):
    payload = {
        "data": {
            "attributes": {
                "accept_translations": True,
                "name": "Resource Name",
                "priority": "normal",
                "slug": f"{resource_slug}",
            },
            "relationships": {
                "i18n_format": {"data": {"id": "KEYVALUEJSON", "type": "i18n_formats"}},
                "project": {
                    "data": {
                        "id": f"o:{config.transifex_organisation_slug}:p:{config.transifex_project_slug}",
                        "type": "projects",
                    }
                },
            },
            "type": "resources",
        }
    }
    resp = requests.post(
        f"{config.transifex_api_url}/resources", headers=headers, json=payload
    )
    resp.raise_for_status()
    return resp.json()


def get_resource(resource_slug: str):
    resp = requests.get(
        f"{config.transifex_api_url}/resources/o:{config.transifex_organisation_slug}:p:{config.transifex_project_slug}:r:{resource_slug}",
        headers=headers,
    )
    if resp.status_code != 200:
        return None
    return resp.json().get("data")


def upload_file(content: Dict[str, str], resource_slug: str):

    payload = {
        "data": {
            "attributes": {
                "callback_url": None,
                "content": json.dumps(content),
                "content_encoding": "text",
            },
            "relationships": {
                "resource": {
                    "data": {
                        "id": f"o:{config.transifex_organisation_slug}:p:{config.transifex_project_slug}:r:{resource_slug}",
                        "type": "resources",
                    }
                }
            },
            "type": "resource_strings_async_uploads",
        }
    }
    resp = requests.post(
        f"{config.transifex_api_url}/resource_strings_async_uploads",
        headers=headers,
        json=payload,
    )
    resp.raise_for_status()


def get_resource_strings(resource_slug: str):
    ret = {}
    has_more = True
    url = f"{config.transifex_api_url}/resource_strings?filter[resource]=o:{config.transifex_organisation_slug}:p:{config.transifex_project_slug}:r:{resource_slug}"
    while has_more:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        resp_json = resp.json()
        has_more = False
        if resp_json.get("links", {}).get("next"):
            has_more = True
            url = resp_json.get("links", {}).get("next")
        for data_item in resp_json.get("data"):
            ret[data_item["attributes"]["key"]] = data_item["attributes"]["strings"]["other"]
    return ret
