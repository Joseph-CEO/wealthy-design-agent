import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
q = json.dumps({'query': 'query { service(id: \"' + svc + '\") { repoTriggers { edges { node { id environmentId } } } } }'}).encode()
r = urllib.request.Request('https://api.railway.app/graphql/v2', data=q, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
try:
    print(json.loads(urllib.request.urlopen(r).read()))
except urllib.error.HTTPError as e:
    print(e.read().decode())
