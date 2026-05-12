import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
tid = '687f2972-ca59-4b50-9fa5-03326c102fde'
api = 'https://api.railway.app/graphql/v2'

q = json.dumps({'query': 'mutation { deploymentTriggerUpdate(id: \"' + tid + '\", input: {rootDirectory: \"backend\"}) { id } }'}).encode()
r = urllib.request.Request(api, data=q, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
try:
    print(json.loads(urllib.request.urlopen(r).read()))
except urllib.error.HTTPError as e:
    print(e.read().decode())
