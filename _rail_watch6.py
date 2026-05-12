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

for i in range(30):
    r = gq('query { service(id: \"' + svc + '\") { deployments(first: 3) { edges { node { id status url } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    if deps:
        d = deps[0]['node']
        print(str(i+1) + ': ' + d['id'][:8] + ' - ' + d['status'])
        if d['status'] in ('SUCCESS','FAILED','CRASHED'):
            if d['status'] == 'FAILED':
                r2 = gq('query { deployment(id: \"' + d['id'] + '\") { meta } }')
                print('Error:', r2.get('data',{}).get('deployment',{}).get('meta',''))
            break
    else:
        print(str(i+1) + ': no deps')
    time.sleep(10)
