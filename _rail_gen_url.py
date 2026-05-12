import urllib.request, json

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
            return {'raw': e.read().decode()[:300]}

# Try to generate a domain
# Use customDomainCreate with a railway.app subdomain
print('=== Trying to generate Railway domain ===')
r = gq('mutation { customDomainCreate(input: {environmentId: \"' + eid + '\", serviceId: \"' + svc + '\", projectId: \"' + pid + '\", domain: \"wealthy-design-api.up.railway.app\"}) { id domain status } }')
print(json.dumps(r, indent=2))

# Check if there's a "create" something for domains
print()
print('=== List customDomainCreate args ===')
r = gq('query { __type(name: \"CustomDomainCreateInput\") { inputFields { name type { name kind } } } }')
print(json.dumps(r, indent=2))
