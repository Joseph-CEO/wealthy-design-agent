import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
did = 'da7dd433-afc8-452c-8ca8-46dfa10bef4e'
api = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

# Check domains on service
r = gq('query { service(id: \"' + svc + '\") { id name domains { edges { node { id domain status } } } } }')
print('Domains:', json.dumps(r, indent=2))

# Check deployment URL
r = gq('query { deployment(id: \"' + did + '\") { id status staticUrl url suggestAddServiceDomain } }')
print('Deployment URL info:', json.dumps(r, indent=2))
