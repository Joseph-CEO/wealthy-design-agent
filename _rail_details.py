import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
svc = 'dfe6b3ee-f9ce-417d-a457-78636bb83cf7'
did = '78010d88-cc8e-4a9c-a50b-c2a84c9d1ede'
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
            return {'raw': e.read().decode()[:300]}

# Check instance details
print('=== Instances ===')
r = gq('query { deployment(id: \"' + did + '\") { instances { id status ... on DeploymentInstance { dockerIp ipAddress ports } } } }')
print(json.dumps(r, indent=2))

# Check volume/config
print()
print('=== Service details ===')
r = gq('query { service(id: \"' + svc + '\") { id name createdAt updatedAt } }')
print(json.dumps(r, indent=2))

# Check environment vars
print()
print('=== Variables ===')
r = gq('query { environment(id: \"' + eid + '\") { variables } }')
print(json.dumps(r, indent=2)[:2000])

# Try the token for an actual web request
print()
print('=== Trying URL directly with different formats ===')
urls = [
    'https://wealthy-design-api.up.railway.app',
    'https://api.up.railway.app',
    'https://' + did + '.up.railway.app',
]
for url in urls:
    print('URL: ' + url)
    # Can't do actual request here but check
