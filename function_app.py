import azure.functions as func
import json
import os
import html
from datetime import datetime, timezone

app = func.FunctionApp()

# ---- Profile data (edit anytime) ----
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


def build_meta():
    # Nice for “version info” on HTML footer + JSON meta
    return {
        "site_name": os.getenv("WEBSITE_SITE_NAME", "unknown"),
        "functions_version": os.getenv("FUNCTIONS_EXTENSION_VERSION", "unknown"),
        "python_version": os.getenv("PYTHON_VERSION", "unknown"),
        # Set this in GitHub Actions as an env var (optional):
        # APP_BUILD_SHA: ${{ github.sha }}
        "build_sha": os.getenv("APP_BUILD_SHA", "local"),
        "utc_time": datetime.now(timezone.utc).isoformat(),
        # Region isn’t reliably exposed as env var; keep as a label
        "region": os.getenv("APP_REGION", "Canada Central")
    }


# ---- One endpoint that can return JSON or HTML ----
@app.route(route="sajbio", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def sajbio(req: func.HttpRequest) -> func.HttpResponse:
    bio = get_bio()
    meta = build_meta()

    # format can be: json | html
    fmt = (req.params.get("format") or "").strip().lower()

    # If user explicitly requests html, return html
    if fmt == "html":
        return _render_html(bio, meta)

    # Default: JSON (or format=json)
    payload = {
        "bio": bio,
        "meta": meta,
        "endpoints": {
            "json": "/api/sajbio",
            "html": "/api/sajbio?format=html"
        }
    }
    return func.HttpResponse(
        body=json.dumps(payload, indent=2),
        status_code=200,
        mimetype="application/json"
    )


# Optional: keep your old URL working (/api/sajbio/html)
@app.route(route="sajbio/html", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def sajbio_html(req: func.HttpRequest) -> func.HttpResponse:
    bio = get_bio()
    meta = build_meta()
    return _render_html(bio, meta)


def _render_html(bio: dict, meta: dict) -> func.HttpResponse:
    name = html.escape(bio["name"])
    headline = html.escape(bio["headline"])
    location = html.escape(bio["location"])
    summary = html.escape(bio["summary"])
    status = html.escape(bio["status"])

    # Links (edit these)
    github_url = html.escape(os.getenv("APP_GITHUB_URL", "https://github.com/sajsamuel"))
    linkedin_url = html.escape(os.getenv("APP_LINKEDIN_URL", "https://www.linkedin.com"))
    email_addr = html.escape(os.getenv("APP_EMAIL", "sajksamuel@outlook.com"))

    skills = "".join(f"<li>{html.escape(s)}</li>" for s in bio["core_expertise"])
    focus = "".join(f"<li>{html.escape(s)}</li>" for s in bio["current_focus"])

    site_name = html.escape(str(meta.get("site_name", "")))
    functions_version = html.escape(str(meta.get("functions_version", "")))
    python_version = html.escape(str(meta.get("python_version", "")))
    build_sha = html.escape(str(meta.get("build_sha", ""))[:7])
    region = html.escape(str(meta.get("region", "")))

    page = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{name} — Bio</title>
  <style>
    :root {{
      --bg: #f6f7fb;
      --card: #ffffff;
      --text: #111827;
      --muted: #6b7280;
      --border: #e5e7eb;
      --pill-bg: #eef2ff;
      --pill-text: #3730a3;
      --btn-bg: #111827;
      --btn-text: #ffffff;
      --btn-muted-bg: #f3f4f6;
      --btn-muted-text: #111827;
      --shadow: 0 8px 24px rgba(0,0,0,0.06);
      --code-bg: #f3f4f6;
    }}

    html[data-theme="dark"] {{
      --bg: #0b1220;
      --card: #0f172a;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --border: #1f2937;
      --pill-bg: #1e293b;
      --pill-text: #c7d2fe;
      --btn-bg: #e5e7eb;
      --btn-text: #111827;
      --btn-muted-bg: #111827;
      --btn-muted-text: #e5e7eb;
      --shadow: 0 10px 30px rgba(0,0,0,0.35);
      --code-bg: #111827;
    }}

    body {{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      margin: 0; padding: 32px;
      background: var(--bg);
      color: var(--text);
    }}

    .card {{
      max-width: 860px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: var(--shadow);
    }}

    .top {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: flex-start;
      justify-content: space-between;
    }}

    h1 {{ margin: 0; font-size: 30px; letter-spacing: -0.02em; }}
    .meta {{ color: var(--muted); margin-top: 6px; }}
    p {{ line-height: 1.65; margin: 14px 0 0 0; }}

    .pill {{
      display: inline-block;
      padding: 8px 12px;
      border-radius: 999px;
      background: var(--pill-bg);
      color: var(--pill-text);
      font-weight: 700;
      font-size: 12px;
      border: 1px solid var(--border);
      white-space: nowrap;
    }}

    .actions {{
      margin-top: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: flex-start;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
      text-decoration: none;
      font-weight: 700;
      font-size: 14px;
      background: var(--btn-muted-bg);
      color: var(--btn-muted-text);
    }}

    .btn.primary {{
      background: var(--btn-bg);
      color: var(--btn-text);
      border-color: transparent;
    }}

    .btn:hover {{ filter: brightness(0.98); }}
    .btn:active {{ transform: translateY(1px); }}

    .toggle {{
      margin-left: auto;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      cursor: pointer;
      font-weight: 700;
    }}

    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 20px;
    }}

    @media (max-width: 760px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .toggle {{ margin-left: 0; }}
    }}

    h2 {{ margin: 0 0 10px 0; font-size: 16px; }}
    ul {{ margin: 8px 0 0 18px; }}
    li {{ margin: 6px 0; }}

    code {{
      background: var(--code-bg);
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 12px;
    }}

    .footer {{
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      display: grid;
      gap: 8px;
      font-size: 13px;
    }}

    .footer .row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: space-between;
      align-items: center;
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

    <div class="actions">
      <a class="btn primary" href="{linkedin_url}" target="_blank" rel="noreferrer">LinkedIn</a>
      <a class="btn" href="{github_url}" target="_blank" rel="noreferrer">GitHub</a>
      <a class="btn" href="mailto:{email_addr}">Email</a>

      <button class="toggle" id="themeToggle" type="button" aria-label="Toggle dark mode">
        🌙 Dark Mode
      </button>
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
      <div class="row">
        <div>JSON: <code>/api/sajbio</code></div>
        <div>HTML: <code>/api/sajbio?format=html</code></div>
      </div>
      <div class="row">
        <div>App: <code>{site_name}</code> • Region: <code>{region}</code></div>
        <div>Functions: <code>{functions_version}</code> • Python: <code>{python_version}</code> • Build: <code>{build_sha}</code></div>
      </div>
    </div>
  </div>

  <script>
    // Dark mode toggle (saved to localStorage)
    const root = document.documentElement;
    const btn = document.getElementById("themeToggle");

    function setTheme(theme) {{
      root.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
      btn.textContent = theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
    }}

    const saved = localStorage.getItem("theme");
    if (saved === "dark" || saved === "light") {{
      setTheme(saved);
    }} else {{
      setTheme("light");
    }}

    btn.addEventListener("click", () => {{
      const current = root.getAttribute("data-theme") || "light";
      setTheme(current === "dark" ? "light" : "dark");
    }});
  </script>
</body>
</html>
"""
    return func.HttpResponse(page, status_code=200, mimetype="text/html")
