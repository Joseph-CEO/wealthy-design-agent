import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
q = json.dumps({'query': '''
query {
  __schema {
    mutationType {
      fields {
        name
        args {
          name
          type { name kind }
        }
      }
    }
  }
}
'''}).encode()
r = urllib.request.Request('https://api.railway.app/graphql/v2', data=q, headers={'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'})
result = json.loads(urllib.request.urlopen(r).read())
if result.get('data'):
    fields = result['data']['__schema']['mutationType']['fields']
    trig_muts = [f['name'] for f in fields if 'trigger' in f['name'].lower()]
    print('Trigger-related mutations:', trig_muts)
    del_muts = [f['name'] for f in fields if 'delete' in f['name'].lower() or 'update' in f['name'].lower()]
    print('Delete/Update mutations:', del_muts[:20])
else:
    print(result)
