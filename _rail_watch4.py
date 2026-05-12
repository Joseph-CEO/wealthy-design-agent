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

print('Waiting for deployment...')
for i in range(36):
    r = gq('query { service(id: \"' + svc + '\") { deployments(first: 1) { edges { node { id status url } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    if deps:
        d = deps[0]['node']
        st = d['status']
        uid = d['id'][:8]
        print(str(i+1) + ': ' + uid + ' - ' + st + ' | URL: ' + str(d.get('url','?')))
        if st in ('SUCCESS','FAILED','CRASHED'):
            if st == 'SUCCESS':
                print('Deployment SUCCESS!')
                print('Full: ' + json.dumps(d, indent=2))
            if st == 'FAILED':
                print('FAILED')
                print('Full: ' + json.dumps(d, indent=2))
            break
    else:
        print('Check ' + str(i+1) + ': No deployments yet')
    time.sleep(10)
