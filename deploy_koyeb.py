import urllib.request, json

TOKEN = "b75af679-4f5f-4dbc-8cb4-39df3c5baf2b"
API = "https://backboard.railway.app/graphql/v2"
PROJECT_ID = "9ed579f0-472a-4a11-a374-0e640fcdc4ab"
ENV_ID = "c776d347-d55e-4aed-ad1d-f828811ef9f2"

def gql(query, vars=None):
    body = {"query": query}
    if vars:
        body["variables"] = vars
    data = json.dumps(body).encode()
    req = urllib.request.Request(API, data=data, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error {e.code}: {body}")
        return None

# Check if "api" service already exists
service_id = None
r = gql('query { project(id: "' + PROJECT_ID + '") { services { edges { node { id name } } } } }')
if r and "data" in r:
    services = r["data"]["project"]["services"]["edges"]
    for s in services:
        if s["node"]["name"] == "api":
            service_id = s["node"]["id"]
            print(f"Found existing service 'api': {service_id}")
            break

# Create service if not found
if not service_id:
    create_mutation = """
    mutation serviceCreate($input: ServiceCreateInput!) {
      serviceCreate(input: $input) { id name }
    }
    """
    create_vars = {
        "input": {
            "projectId": PROJECT_ID,
            "name": "api",
            "source": {"repo": "Joseph-CEO/wealthy-design-agent"},
            "branch": "main",
            "variables": [
                {"key": "ADMIN_TOKEN", "value": "admin-secret-token-2024"},
                {"key": "SENDER_EMAIL", "value": "hello@wealthydesign.co.ke"},
                {"key": "SENDER_NAME", "value": "Wealthy Design Agency"},
                {"key": "FRONTEND_URL", "value": "https://frontend-iota-rust-82.vercel.app"},
                {"key": "CORS_ORIGINS", "value": "https://frontend-iota-rust-82.vercel.app,http://localhost:3000"}
            ]
        }
    }
    r = gql(create_mutation, create_vars)
    if r and "data" in r:
        service_id = r["data"]["serviceCreate"]["id"]
        print(f"Service created: {service_id}")
    else:
        print("Failed to create service")
        exit(1)

# Configure service instance (Dockerfile, scaling, health check, region)
update_mutation = """
mutation serviceInstanceUpdate($serviceId: String!, $environmentId: String!, $input: ServiceInstanceUpdateInput!) {
  serviceInstanceUpdate(serviceId: $serviceId, environmentId: $environmentId, input: $input)
}
"""
update_vars = {
    "serviceId": service_id,
    "environmentId": ENV_ID,
    "input": {
        "dockerfilePath": "backend/Dockerfile",
        "rootDirectory": "backend",
        "startCommand": "sh -c 'uvicorn app.main:app --host 0.0.0.0 --port $PORT'",
        "healthcheckPath": "/api/v1/health",
        "healthcheckTimeout": 600,
        "numReplicas": 1,
        "region": "us-west1",
        "restartPolicyType": "ON_FAILURE",
        "restartPolicyMaxRetries": 3,
        "sleepApplication": true
    }
}
r = gql(update_mutation, update_vars)
if r:
    print(f"Service instance updated: {r}")

# Trigger deployment
deploy_mutation = """
mutation serviceInstanceDeployV2($serviceId: String!, $environmentId: String!) {
  serviceInstanceDeployV2(serviceId: $serviceId, environmentId: $environmentId)
}
"""
deploy_vars = {"serviceId": service_id, "environmentId": ENV_ID}
r = gql(deploy_mutation, deploy_vars)
if r and "data" in r:
    deployment_id = r["data"]["serviceInstanceDeployV2"]
    print(f"Deployment triggered! ID: {deployment_id}")

# Create public domain
domain_mutation = """
mutation serviceDomainCreate($input: ServiceDomainCreateInput!) {
  serviceDomainCreate(input: $input) { domain }
}
"""
domain_vars = {
    "input": {
        "environmentId": ENV_ID,
        "serviceId": service_id,
        "targetPort": 8080
    }
}
r = gql(domain_mutation, domain_vars)
if r and "data" in r:
    print(f"URL: https://{r['data']['serviceDomainCreate']['domain']}/api/v1/health")
