#--- Standalone script to request API token ---
#Returns token from API for valid user credentials

import requests
import json

#Get user credentials
user = input('Username: ')

pwd = input('Password: ')

#Create request
headers = {'Content-Type': 'application/json'}
api_endpoint = 'http://127.0.0.1:8000/get-api-token/'
request = {'username':user, 'password':pwd}
r = requests.post(url = api_endpoint, json = request, headers=headers).json()

#Print response
try:
    print('\nToken = ' + r['token'] + '\n')
except KeyError:
    print(r)
