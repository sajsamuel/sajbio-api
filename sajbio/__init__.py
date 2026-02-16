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

    # Escape text for safety in HTML
    name = html.escape(bio["name"])
    headline = html.escape(bio["headline"])
    location = html.escape(bio["location"])
    summary = html.escape(bio["summary"])
    status = html.escape(bio["status"])

    skills = "".join(f"<li>{html.escape(s)}</li>" for s in bio["core_expertise"])
    focus = "".join(f"<li>{html.escape(s)}</li>" for s in bio["current_focus"])

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{name} — Bio</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      margin: 0; padding: 32px;
      background: #f6f7fb;
      color: #111827;
    }}
    .card {{
      max-width: 820px;
      margin: 0 auto;
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    }}
    .top {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: baseline;
      justify-content: space-between;
    }}
    h1 {{ margin: 0; font-size: 28px; }}
    .meta {{ color: #6b7280; }}
    .pill {{
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: #eef2ff;
      color: #3730a3;
      font-weight: 600;
      font-size: 12px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 18px;
    }}
    @media (max-width: 720px) {{
      .grid {{ grid-template-columns: 1fr; }}
    }}
    h2 {{ margin: 0 0 8px 0; font-size: 16px; }}
    p {{ line-height: 1.6; margin: 10px 0 0 0; }}
    ul {{ margin: 8px 0 0 18px; }}
    .footer {{
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid #e5e7eb;
      color: #6b7280;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: space-between;
      font-size: 13px;
    }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{
      background: #f3f4f6;
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="top">
      <div>
        <h1>{name}</h1>
        <div class="meta">{headline} • {location}</div>
      </div>
      <div class="pill">{status}</div>
    </div>

    <p>{summary}</p>

    <div class="grid">
      <div>
        <h2>Core Expertise</h2>
        <ul>{skills}</ul>
      </div>
      <div>
        <h2>Current Focus</h2>
        <ul>{focus}</ul>
      </div>
    </div>

    <div class="footer">
      <div>JSON endpoint: <code>/api/sajbio</code></div>
      <div>HTML endpoint: <code>/api/sajbio/html</code></div>
    </div>
  </div>
</body>
</html>
"""

    return func.HttpResponse(page, status_code=200, mimetype="text/html")
