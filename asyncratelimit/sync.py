import httpx

results = []
for x in range(1,1000):
    resp = httpx.get("http://localhost:4000")
    results.append(resp.json())
    print(x)


errors = sum([1 for e in results if 'Error' in e.values()])
sucesses = sum([1 for e in results if 'Successful' in e.values()])
output = {"sucesses": sucesses, "errors": errors}
print(output)
