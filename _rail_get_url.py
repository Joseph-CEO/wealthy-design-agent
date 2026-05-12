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

for i in range(6):
    r = gq('query { service(id: "' + svc + '") { deployments(last: 1) { edges { node { id status url } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    if deps:
        d = deps[0]['node']
        print('Status:', d['status'], '| URL:', d.get('url','(none)'))
        if d['status'] == 'SUCCESS':
            # Also check for custom domains
            r2 = gq('query { service(id: "' + svc + '") { id name } }')
            print('Service:', json.dumps(r2, indent=2))
            break
    time.sleep(5)
