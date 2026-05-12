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
        try:
            return json.loads(e.read().decode())
        except:
            return {'raw': e.read().decode()[:300]}

# Look for how to make a service serverless
# Try checking if serviceUpdate supports sleepApplication
r = gq("""query { __type(name: \"ServiceUpdateInput\") { inputFields { name type { name kind } } } }""")
print('ServiceUpdateInput:', json.dumps(r, indent=2))

# Try deploymentTriggerUpdate
r = gq("""query { __type(name: \"DeploymentTriggerUpdateInput\") { inputFields { name type { name kind } } } }""")
print('DeploymentTriggerUpdateInput:', json.dumps(r, indent=2))

# Maybe there is an environment-level serverless setting
r = gq("""query { __type(name: \"Environment\") { fields { name } } }""")
if r.get('data'):
    srv_fields = [f['name'] for f in r['data']['__type']['fields'] if 'sleep' in f['name'].lower() or 'server' in f['name'].lower()]
    print('Environment sleep/serverless fields:', srv_fields)
