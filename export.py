#!/usr/bin/env python
import requests
import json

username = 'admin'
password = 'Arista'
server1 = 'https://192.168.255.50'
csvfilename = 'inventory.csv'

connect_timeout = 10
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
requests.packages.urllib3.disable_warnings()
session = requests.Session()

def login(url_prefix, username, password):
    authdata = {"userId": username, "password": password}
    headers.pop('APP_SESSION_ID', None)
    response = session.post(url_prefix+'/web/login/authenticate.do', data=json.dumps(authdata),
                            headers=headers, timeout=connect_timeout,
                            verify=False)
    cookies = response.cookies
    headers['APP_SESSION_ID'] = response.json()['sessionId']
    if response.json()['sessionId']:
        return response.json()['sessionId']

def get_inventory(url_prefix):
    response = session.get(url_prefix+'/cvpservice/inventory/devices')
    return response.json()

device_list = []
print '###### Logging into Server 1'
login(server1, username, password)
inventory = get_inventory(server1)
with open(csvfilename, 'w') as f:
  f.write('hostname,modelName,systemMacAddress,version,serialNumber,ipAddress\n')
  for switch in inventory:
      hostname = switch['hostname']
      print hostname
      f.write(hostname+',')
      modelName = switch['modelName']
      f.write(modelName+',')
      systemMacAddress = switch['systemMacAddress']
      f.write(systemMacAddress+',')
      version = switch['version']
      f.write(version+',')
      serialNumber = switch['serialNumber']
      f.write(serialNumber+',')
      ipAddress = switch['ipAddress']
      f.write(ipAddress+'\n')
      device_list.append({hostname: {'model' : modelName, 'mac': systemMacAddress, 'version': version, 'mgmtIP': ipAddress}})
f.close()
print '##### Complete'
