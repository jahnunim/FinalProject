import requests
url = 'http://127.0.0.1:5000/tests?domain=nice.com&test=SPF'

response = requests.get(url)
print (response.text)
print (response.json())