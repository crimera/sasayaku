import urllib.parse
import requests
import json
import ast

ENDPOINT = "https://api.asmr-100.com/api/tracks/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"}

def getDir(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        query_dict = urllib.parse.parse_qs(parsed_url.query)
        path_list = ast.literal_eval(query_dict['path'][0])
        return path_list
    except (KeyError, ValueError):
        # No path query parameter or not a valid list expression
        return []

def getCode(url: str):
    path = urllib.parse.urlparse(url).path
    code = path.split('/')[-1]
    return code.replace('RJ', '')

def getWork(code: str):
    url = ENDPOINT + code
    response = requests.get(url, headers=HEADERS)
    return response.json()

def getTrackUrls(path: dict, json):
    if len(path) == 0: return json
    for child in json:
        if child['title'] == path[0]:
            json = child['children']
            del path[0]
            return getTrackUrls(path, json)
    return json

url = "https://asmr.one/work/RJ01032675?path=%5B%22mp3%5B320kbps%5D%22,%2201_%E6%9C%AC%E7%B7%A8%22%5D#work-tree"
directory = getDir(url)
code = getCode(url)
tree = getWork(code)
links = getTrackUrls(directory, tree)
print(links[0]['mediaDownloadUrl'])
