import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
did = 'da7dd433-afc8-452c-8ca8-46dfa10bef4e'
api = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())

r = gq('query { deployment(id: \"' + did + '\") { id status url meta instances { id status } } }')
print(json.dumps(r, indent=2))
