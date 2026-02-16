import azure.functions as func

app = func.FunctionApp()

@app.route(route="sajbio", auth_level=func.AuthLevel.ANONYMOUS)
def sajbio(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        '{"name":"Saj Samuel","title":"Azure Builder"}',
        mimetype="application/json"
    )
