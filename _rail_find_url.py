import urllib.request, json, time

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
pid = '9ed579f0-472a-4a11-a374-0e640fcdc4ab'
eid = 'c776d347-d55e-4aed-ad1d-f828811ef9f2'
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
            return {'raw': e.read().decode()[:200]}

# List all domains
print('=== All custom domains ===')
r = gq('query { project(id: \"' + pid + '\") { customDomains { edges { node { id domain status { verified } } } } } }')
print(json.dumps(r, indent=2))

# Check deployment URL again (maybe populated now)
print()
print('=== Deployment URL ==')
r = gq('query { deployment(id: \"78010d88-cc8e-4a9c-a50b-c2a84c9d1ede\") { id status url staticUrl } }')
print(json.dumps(r, indent=2))
