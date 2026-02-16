import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"name": "Saj Samuel", "title": "Azure Builder"}),
        mimetype="application/json",
        status_code=200
    )
