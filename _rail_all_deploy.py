import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
api = 'https://api.railway.app/graphql/v2'
q = json.dumps({'query': 'query { service(id: \"' + svc + '\") { deployments { edges { node { id status createdAt url staticUrl } } } } }'}).encode()
r = urllib.request.Request(api, data=q, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
print(json.loads(urllib.request.urlopen(r).read()))
