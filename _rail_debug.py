import urllib.request, json
t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
did = '7b849064-1d8a-4098-909b-58efec7b254c'
api = 'https://api.railway.app/graphql/v2'
def gq(q):
    d = json.dumps({'query': q}).encode()
    r = urllib.request.Request(api, data=d, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
r = gq('query { deployment(id: \"' + did + '\") { id status meta } }')
meta = r.get('data',{}).get('deployment',{}).get('meta',{})
print('Status:', r.get('data',{}).get('deployment',{}).get('status'))
print('Builder:', meta.get('serviceManifest',{}).get('build',{}).get('builder'))
print('Dockerfile:', meta.get('serviceManifest',{}).get('build',{}).get('dockerfilePath'))
print('RootDir:', meta.get('rootDirectory'))
print('Commit:', meta.get('commitMessage'))
print('ConfigFile:', meta.get('configFile'))
print(json.dumps(r, indent=2)[:2000])
