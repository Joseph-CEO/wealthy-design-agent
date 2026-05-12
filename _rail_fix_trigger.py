import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
tid = '687f2972-ca59-4b50-9fa5-03326c102fde'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
api = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except:
            return {'raw': e.read().decode()[:300]}

# First get trigger to confirm the ID
print('=== Current trigger ===')
r = gq('query { service(id: \"' + svc + '\") { repoTriggers { edges { node { id environmentId } } } } }')
print(json.dumps(r, indent=2))

# Delete the old trigger
print()
print('=== Deleting trigger ===')
r = gq('mutation { deploymentTriggerDelete(id: \"' + tid + '\") }')
print(json.dumps(r, indent=2))

# Create new trigger WITHOUT rootDirectory
print()
print('=== Creating new trigger without rootDirectory ===')
pid = '9ed579f0-472a-4a11-a374-0e640fcdc4ab'
eid = 'c776d347-d55e-4aed-ad1d-f828811ef9f2'
r = gq('mutation { deploymentTriggerCreate(input: {serviceId: \"' + svc + '\", projectId: \"' + pid + '\", environmentId: \"' + eid + '\", branch: \"main\", repository: \"Joseph-CEO/wealthy-design-agent\", provider: \"github\"}) { id } }')
print(json.dumps(r, indent=2))
