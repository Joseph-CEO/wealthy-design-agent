import urllib.request, json

TOKEN = "c41152ff-2b5b-4155-898b-50edcf3eb75c"
DEP_ID = "f0742a8a-02dc-4867-835a-a40273fb897f"
API = "https://api.railway.app/graphql/v2"

def gql(query):
    data = json.dumps({"query": query}).encode()
    req = urllib.request.Request(API, data=data, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except:
            return {"raw": e.read().decode()[:500]}

# Check deployment status
r = gql(f'query {{ deployment(id: "{DEP_ID}") {{ id status url staticUrl createdAt diagnosis }} }}')
print(json.dumps(r, indent=2))

# Redeploy
r = gql(f'mutation {{ deploymentRedeploy(id: "{DEP_ID}") {{ id status url }} }}')
print(json.dumps(r, indent=2))
