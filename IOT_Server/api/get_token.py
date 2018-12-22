import requests
import json

#Returns key from username and password

#Get user credentials
user = input('Username: ')

pwd = input('Password: ')

#Create request
headers = {'Content-Type': 'application/json'}
api_endpoint = 'http://127.0.0.1:8000/get-api-token/'
request = {'username':user, 'password':pwd}
r = requests.post(url = api_endpoint, json = request, headers=headers).json()
try:
    print('\nToken = ' + r['token'] + '\n')
except KeyError:
    print(r)
