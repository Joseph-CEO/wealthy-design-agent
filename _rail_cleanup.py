import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
pid = '9ed579f0-472a-4a11-a374-0e640fcdc4ab'
eid = 'c776d347-d55e-4aed-ad1d-f828811ef9f2'
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

print('Project:', json.dumps(gq('query { project(id: \"' + pid + '\") { id name } }'), indent=2))
print('Service:', json.dumps(gq('query { service(id: \"' + svc + '\") { id name } }'), indent=2))
print('Env:', json.dumps(gq('query { environment(id: \"' + eid + '\") { id name } }'), indent=2))

# Check all services in project
print()
print('All services:')
r = gq('query { project(id: \"' + pid + '\") { services { edges { node { id name } } } } }')
print(json.dumps(r, indent=2))
