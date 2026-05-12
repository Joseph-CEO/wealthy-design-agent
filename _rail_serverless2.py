import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
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

# Search for types containing 'deploy' or 'service' config
r = gq("""
query {
  __schema {
    types {
      name
    }
  }
}
""")
if r.get('data'):
    names = [t['name'] for t in r['data']['__schema']['types'] if 'Deploy' in t['name'] or 'Service' in t['name'] if t['name'].startswith('__') == False]
    print('Deploy/Service related types:')
    for n in sorted(names)[:30]:
        print('  ' + n)
