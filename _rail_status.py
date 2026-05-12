import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
api = 'https://api.railway.app/graphql/v2'
def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
r = gq('query { service(id: \"' + svc + '\") { deployments(first: 3) { edges { node { id status createdAt url staticUrl } } } } }')
print(json.dumps(r, indent=2))
