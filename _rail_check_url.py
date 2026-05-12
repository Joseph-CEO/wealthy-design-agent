import urllib.request, json, time

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
did = '78010d88-cc8e-4a9c-a50b-c2a84c9d1ede'
api = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

print('Checking deployment instances...')
for i in range(6):
    r = gq('query { deployment(id: \"' + did + '\") { id status instances { id status } } }')
    print(r.get('data',{}).get('deployment',{}))
    time.sleep(5)

print()
print('Deployment meta:')
r = gq('query { deployment(id: \"' + did + '\") { id status url staticUrl meta } }')
print(json.dumps(r, indent=2))
