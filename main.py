from random import randint
from requests import get
from flask import Flask, Response, request

app = Flask(__name__)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/")
def root():
    return "Proxy is Running!"


@app.route("/get/<path:path>", methods=['GET'])
def proxy(path):
    headers = {
        "User-Agent": f"Proxy - {randint(1, 100)}!"
    }
    request_headers = dict(request.headers)
    try:
        if request_headers["Library"] == "ScratchConnect.py":
            try:
                response = get(path, params=dict(request.args))
                raw_headers = response.raw.headers.items()
                excluded_headers = ["content-encoding"]
                headers = []
                for (name, value) in raw_headers:
                    if name.lower() not in excluded_headers:
                        headers.append((name, value))
                return Response(response.content, response.status_code, headers)
            except Exception as E:
                return Response("Internal Server Error - " + str(E), status=500)
        else:
            return Response("Access Denied!", status=403)
    except KeyError:
        return Response("Access Denied!", status=403)
