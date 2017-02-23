import requests
host='http://127.0.0.1:8000/'
r=requests.get(host)
print(r.json)
