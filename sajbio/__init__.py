import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    bio = {
        "name": "Saj Samuel",
        "title": "Data Engineer / SQL Developer",
        "location": "New Hyde Park, NY",
        "skills": ["Azure", "SQL Server", "Python", "ETL"],
        "current_focus": "Building Azure Serverless Applications"
    }
    return func.HttpResponse(json.dumps(bio), mimetype="application/json")
