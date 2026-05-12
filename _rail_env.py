import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
pid = '9ed579f0-472a-4a11-a374-0e640fcdc4ab'
eid = 'c776d347-d55e-4aed-ad1d-f828811ef9f2'
api = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

# Get environment variables
print('=== Environment variables ===')
r = gq('query { environment(id: \"' + eid + '\") { id name variables { name value } } }')
print(json.dumps(r, indent=2))

# Try to access via Railway default URL pattern
# Check if there's a project-level domain
print()
print('=== Project info ===')
r = gq('query { project(id: \"' + pid + '\") { id name description isPublic } }')
print(json.dumps(r, indent=2))
