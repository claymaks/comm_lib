import requests
for i in range(10):
    requests.put('http://172.20.10.2:5000/', data={'data':"123456"})
print(requests.get('http://172.20.10.2:5000/').json())
print(requests.delete('http://172.20.10.2:5000/', data={'data':"123456"}).json())