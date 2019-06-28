#!/usr/bin/env python
import requests
import json

username = 'admin'
password = 'Arista'
server1 = 'https://192.168.255.51'
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

def old_get_inventory(url_prefix):
    response = session.get(url_prefix+'/cvpservice/inventory/getInventory.do?startIndex=0&endIndex=0')
    return response.json()

def get_inventory(url_prefix):
    response = session.get(url_prefix+'/cvpservice/inventory/devices')
    return response.json()

device_list = []
print '###### Logging into Server 1'
login(server1, username, password)
try:
    inventory = get_inventory(server1)
    if inventory:
        apiversion = 'new'
except:
    apiversion = 'old'
    inventory = old_get_inventory(server1)['netElementList']
with open(csvfilename, 'w') as f:
  f.write('hostname,modelName,systemMacAddress,version,serialNumber,ipAddress\n')
  for switch in inventory:
      if apiversion == 'new':
          hostname = switch['hostname']
      else:
          hostname = switch['fqdn']
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
