import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="sajbio", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def sajbio(req: func.HttpRequest) -> func.HttpResponse:
    bio = {
        "name": "Saj Samuel",
        "headline": "Data Engineer | Azure | SQL",
        "location": "New Hyde Park, NY",
        "summary": (
            "Data-focused technology professional specializing in SQL Server, "
            "T-SQL optimization, financial data systems, and Azure-based cloud solutions. "
            "Experienced in building ETL/ELT pipelines, automation workflows, "
            "reporting systems, and modernizing enterprise data architectures."
        ),
        "core_expertise": [
            "SQL Server & T-SQL",
            "Stored Procedures & Performance Tuning",
            "ETL / ELT Pipelines",
            "Azure Functions (Serverless)",
            "GitHub Actions CI/CD",
            "SSRS Reporting",
            "Financial & Cost Data Systems",
            "Process Automation"
        ],
        "current_focus": [
            "Azure Serverless Architecture",
            "Cloud-native App Development",
            "Data Engineering Best Practices",
            "AI-powered Enterprise Solutions"
        ],
        "status": "Actively building modern Azure-based data solutions"
    }

    return func.HttpResponse(
        body=json.dumps(bio, indent=2),
        status_code=200,
        mimetype="application/json"
    )
