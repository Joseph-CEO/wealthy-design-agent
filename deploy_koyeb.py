import urllib.request, json

# Check if koyeb CLI is available or API endpoint
TOKEN = "7da072b7-d808-456c-acd6-270fdb9037e3"

# Test Koyeb API
req = urllib.request.Request("https://app.koyeb.com/v1/account")
req.add_header("Authorization", f"Bearer {TOKEN}")
try:
    resp = urllib.request.urlopen(req)
    print("Koyeb:", resp.read().decode())
except urllib.error.HTTPError as e:
    print(f"Koyeb Error {e.code}: {e.read().decode()[:200]}")
except Exception as e:
    print(f"Koyeb Error: {e}")

# Test Railway v5 API
query = '{"query":"{projects{edges{node{id name}}}}"}'
req2 = urllib.request.Request("https://backboard.railway.app/graphql/v2", data=query.encode(), headers={
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
})
try:
    resp2 = urllib.request.urlopen(req2)
    print("Railway v5:", resp2.read().decode()[:300])
except urllib.error.HTTPError as e:
    print(f"Railway v5 Error {e.code}")
    print(e.read().decode()[:200])
except Exception as e:
    print(f"Railway v5 Error: {e}")
