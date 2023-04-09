import urllib.parse
import requests
import json
import ast

ENDPOINT = "https://api.asmr-100.com/api/tracks/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"}


def get_dir(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        query_dict = urllib.parse.parse_qs(parsed_url.query)
        path_list = ast.literal_eval(query_dict['path'][0])
        return path_list
    except (KeyError, ValueError):
        # No path query parameter or not a valid list expression
        return []


def get_code(url: str):
    path = urllib.parse.urlparse(url).path
    code = path.split('/')[-1]
    return code.replace('RJ', '')


def get_work(code: str):
    url = ENDPOINT + code
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_track_urls(path: dict, data):
    if len(path) == 0:
        return data
    for child in data:
        if child['title'] == path[0]:
            del path[0]
            return get_track_urls(path, child['children'])
    return data
