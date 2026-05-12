import urllib.request, json, time

T = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
DEP_ID = '575a1ce7-a9d6-49c6-9304-a25e1f675512'
API = 'https://api.railway.app/graphql/v2'

def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(API, data=d, headers={'Authorization': 'Bearer '+T, 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(r).read())

for i in range(12):
    r = gq(f'query {{ deployment(id: "{DEP_ID}") {{ id status url }} }}')
    print(f'Check {i+1}: {r.get("data",{}).get("deployment",{}).get("status")}')
    st = r.get('data',{}).get('deployment',{}).get('status','')
    if st in ('SUCCESS','FAILED','CRASHED'):
        print(json.dumps(r, indent=2))
        break
    time.sleep(10)
