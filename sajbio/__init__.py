import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    data = {"name": "Saj Samuel", "title": "Azure Builder"}
    return func.HttpResponse(
        body=json.dumps(data),
        status_code=200,
        mimetype="application/json"
    )
