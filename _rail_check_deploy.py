import urllib.request, json

t = 'c41152ff-2b5b-4155-898b-50edcf3eb75c'
did = 'be255b8d-e4a5-437b-adbb-da6d53bbf142'
api = 'https://api.railway.app/graphql/v2'
q = json.dumps({'query': 'query { deployment(id: \"' + did + '\") { id status meta } }'}).encode()
r = urllib.request.Request(api, data=q, headers={'Authorization': 'Bearer '+t, 'Content-Type': 'application/json'})
try:
    result = json.loads(urllib.request.urlopen(r).read())
    meta = result.get('data',{}).get('deployment',{}).get('meta',{})
    print('RootDirectory:', meta.get('rootDirectory'))
    print('Builder:', meta.get('serviceManifest',{}).get('build',{}).get('builder'))
    print('DockerfilePath:', meta.get('serviceManifest',{}).get('build',{}).get('dockerfilePath'))
    print('BuildCommand:', meta.get('serviceManifest',{}).get('build',{}).get('buildCommand'))
    print('StartCommand:', meta.get('serviceManifest',{}).get('deploy',{}).get('startCommand'))
    print(json.dumps(result, indent=2)[:3000])
except urllib.error.HTTPError as e:
    print(e.read().decode())
