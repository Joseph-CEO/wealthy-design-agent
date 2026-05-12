import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
q = json.dumps({'query': '''
query {
  __type(name: "Service") {
    fields { name }
  }
}
'''}).encode()
r = urllib.request.Request('https://api.railway.app/graphql/v2', data=q, headers={'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'})
print(json.loads(urllib.request.urlopen(r).read()))
