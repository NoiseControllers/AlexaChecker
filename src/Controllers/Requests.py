import requests

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


def requests_get(url, **kwargs):
    try:
        resp = requests.get(url, headers=HEADERS, **kwargs)
    except Exception:
        resp = None

    return resp
