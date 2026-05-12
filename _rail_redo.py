import urllib.request, json, time

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

# Delete the REMOVED deployment via redeploying
# Actually let me just check the current status and trigger a fresh deploy
r = gq('query { service(id: \"' + svc + '\") { id name deployments(first: 1) { edges { node { id status url } } } } }')
print('Latest deployment:', json.dumps(r, indent=2))

# We need to get a SUCCESS deployment. Maybe push another commit?
# Or just trigger a redeploy
