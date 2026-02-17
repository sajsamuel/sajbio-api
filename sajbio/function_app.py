import azure.functions as func
import json
import html

app = func.FunctionApp()

def get_bio():
    return {
        "name": "Saj Samuel",
        "headline": "Data Engineer | Azure | SQL",
        "location": "New Hyde Park, NY",
        "summary": (
            "Data-focused technology professional specializing in SQL Server, "
            "T-SQL optimization, financial data systems, and Azure-based cloud solutions. "
            "Experienced in building ETL/ELT pipelines, automation workflows, reporting systems, "
            "and modernizing enterprise data architectures."
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

@app.route(route="sajbio", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def sajbio(req: func.HttpRequest) -> func.HttpResponse:
    bio = get_bio()
    return func.HttpResponse(
        body=json.dumps(bio, indent=2),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="sajbio/html", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def sajbio_html(req: func.HttpRequest) -> func.HttpResponse:
    bio = get_bio()

    name = html.escape(bio["name"])
    headline = html.escape(bio["headline"])
    location = html.escape(bio["location"])
    summary = html.escape(bio["summary"])
    status = html.escape(bio["status"])

    skills = "".join(f"<li>{html.escape(s)}</li>" for s in bio["core_expertise"])
    focus = "".join(f"<li>{html.escape(s)}</li>" for s in bio["current_focus"])

    page = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — Bio</title></head>
<body style="font-family:Segoe UI, Arial, sans-serif; padding:24px; background:#f6f7fb;">
  <div style="max-width:820px;margin:0 auto;background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:22px;">
    <h1 style="margin:0;">{name}</h1>
    <div style="color:#6b7280;margin-top:6px;">{headline} • {location}</div>
    <div style="margin-top:14px;color:#111827;">{summary}</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px;">
      <div>
        <h3 style="margin:0 0 8px 0;">Core Expertise</h3>
        <ul>{skills}</ul>
      </div>
      <div>
        <h3 style="margin:0 0 8px 0;">Current Focus</h3>
        <ul>{focus}</ul>
      </div>
    </div>

    <div style="margin-top:18px;padding-top:12px;border-top:1px solid #e5e7eb;color:#6b7280;">
      <div>JSON: <code>/api/sajbio</code></div>
      <div>HTML: <code>/api/sajbio/html</code></div>
      <div style="margin-top:6px;font-weight:600;">{status}</div>
    </div>
  </div>
</body></html>
"""
    return func.HttpResponse(page, status_code=200, mimetype="text/html")
