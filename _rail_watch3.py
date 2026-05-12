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

print('Waiting for new deployment...')
for i in range(30):
    r = gq('query { service(id: "' + svc + '") { deployments(first: 1) { edges { node { id status createdAt url } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    if deps:
        d = deps[0]['node']
        st = d['status']
        uid = d['id'][:8]
        url = d.get('url','')
        print(str(i+1) + ': ' + uid + ' - ' + st)
        if st in ('SUCCESS','FAILED','CRASHED'):
            print(json.dumps(d, indent=2))
            if st == 'FAILED':
                q2 = json.dumps({'query': 'query { deployment(id: \"' + d['id'] + '\") { id status meta } }'}).encode()
                r2 = urllib.request.Request(api, data=q2, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
                m = json.loads(urllib.request.urlopen(r2).read())
                mm = m.get('data',{}).get('deployment',{}).get('meta',{})
                print('rootDirectory:', mm.get('rootDirectory'))
                print('builder:', mm.get('serviceManifest',{}).get('build',{}).get('builder'))
                print('dockerfilePath:', mm.get('serviceManifest',{}).get('build',{}).get('dockerfilePath'))
            if st == 'SUCCESS' and url:
                print('Backend URL: https://' + url)
            break
    else:
        print('Check ' + str(i+1) + ': No deployments yet')
    time.sleep(10)
