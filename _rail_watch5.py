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

print('Watching for new deployment...')
seen = set()
for i in range(36):
    r = gq('query { service(id: \"' + svc + '\") { deployments(last: 3) { edges { node { id status url staticUrl } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    for dep in deps:
        n = dep['node']
        uid = n['id'][:8]
        if uid not in seen:
            seen.add(uid)
            print(str(i+1) + ': NEW ' + uid + ' - ' + n['status'] + ' | URL: ' + str(n.get('url','?')))
        if n['status'] in ('SUCCESS','FAILED','CRASHED') and uid in seen:
            pass  # already printed
    # Check if newest is successful
    if deps:
        newest = deps[0]['node']
        if newest['status'] == 'SUCCESS' and newest.get('url'):
            print('SUCCESS with URL: ' + str(newest.get('url')))
            break
        if newest['status'] in ('FAILED','CRASHED'):
            print('Latest: ' + newest['status'])
            break
    time.sleep(10)
