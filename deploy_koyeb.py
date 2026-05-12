import urllib.request, json

TOKEN = "v62xbfyuh9kbze2lmsicskjvhwmsdmqcd2xsv9gvz1za50j0yrtwvokasaj660tc"
API = "https://app.koyeb.com/v1"
APP_ID = "1db625f1-65ae-4e45-887d-a63c80d9e991"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

service_body = {
    "app_id": APP_ID,
    "type": "web",
    "name": "api",
    "definition": {
        "name": "api",
        "scalings": [
            {"min": 1, "max": 1}
        ],
        "instance_types": [
            {"min_scale": 1, "max_scale": 1, "type": "nano"}
        ],
        "git": {
            "repository": "github.com/Joseph-CEO/wealthy-design-agent",
            "branch": "main",
            "no_deploy_on_push": False,
            "dockerfile_path": "backend/Dockerfile"
        },
        "ports": [
            {"port": 8000, "protocol": "http"}
        ],
        "env": [
            {"key": "ADMIN_TOKEN", "value": "admin-secret-token-2024"},
            {"key": "SENDER_EMAIL", "value": "hello@wealthydesign.co.ke"},
            {"key": "SENDER_NAME", "value": "Wealthy Design Agency"},
            {"key": "FRONTEND_URL", "value": "https://frontend-iota-rust-82.vercel.app"}
        ],
        "regions": ["par"],
        "health_check": {"path": "/api/v1/health"}
    }
}

req = urllib.request.Request(
    f"{API}/services",
    data=json.dumps(service_body).encode(),
    headers=headers,
    method="POST"
)
try:
    resp = urllib.request.urlopen(req)
    print("Service created successfully!")
    print(json.dumps(json.loads(resp.read()), indent=2)[:1000])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body}")
