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
prev_count = 0
for i in range(30):
    r = gq('query { service(id: \"' + svc + '\") { deployments { edges { node { id status url createdAt } } } } }')
    deps = r.get('data',{}).get('service',{}).get('deployments',{}).get('edges',[])
    count = len(deps)
    newest = deps[0]['node'] if deps else None
    if count > prev_count:
        print('NEW deployment: ' + newest['id'][:8] + ' - ' + newest['status'])
        prev_count = count
    if newest and newest['status'] in ('SUCCESS','FAILED','CRASHED'):
        print('Final: ' + newest['id'][:8] + ' - ' + newest['status'] + ' | URL: ' + str(newest.get('url')))
        if newest['status'] == 'SUCCESS':
            print(json.dumps(newest, indent=2))
        break
    time.sleep(10)
