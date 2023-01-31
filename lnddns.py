from linode_api4 import LinodeClient
from datetime import datetime
from requests import get
import configparser

#  Put all the configuration setup into a single function
def loadConfig(entry):
    config = configparser.ConfigParser()
    config.read('lnddns.conf')
    
    # This is the Linode API Token to access the Linode DNS configuration.
    # It can be reached at https://cloud.linode.com/profile/tokens 
    if entry == 'token':
        if not 'Linode Token' in config:
            print("[Linode Token] configurations section missing")
            exit(100)
        
        tokenEntry = config['Linode Token']
        return tokenEntry.get('token','')

    # This accesses the domain and server names that need to be set to the current public IP address.
    # The varable names are domainX and serverX with each successive lookup replacing X with an incremental number.
    # E.g.  domain1, server1; domain2, server2; domain3, server3......
    # You can have as many domain, server pairs as you want.
    if entry[:6] == 'domain' or entry[:6] == 'server':
        recordsEntry = config['records']
        return recordsEntry.get(entry,'')
    
    
    if entry == 'myipurl':
        recordsEntry = config['myip']
        return recordsEntry.get(entry,'')
    
    return ""


# This gets the current public ip of this computer and returns the value as a string containing only the IP address.
def getPublicIP():
    return get(loadConfig('myipurl')).text


token = loadConfig('token')
if token == '':
    print("'token' value missing from [Linode Token] configutation section")
    exit(100)

actualIp = getPublicIP()
client = LinodeClient(token)
domainList = client.domains().lists[0]
print('Checking DNS at ' + datetime.now().strftime('%d-%b-%Y (%H:%M:%S.%f)'))


serverEntry = 1

while not serverEntry == 0:
    domainFound = False
    serverFound = False

    domain = loadConfig('domain' + str(serverEntry))
    server = loadConfig('server' + str(serverEntry))

    if domain == '':
        break

    for linodeDomain in domainList:
        if linodeDomain.domain == domain:
            domainFound = True
            print('\n' + linodeDomain.domain + " domain found")
            break

    if domainFound == False:
        print("Domain " + domain + " not found")
        exit(2)

    for linodeServer in linodeDomain.records:
        if linodeServer.name == server:
            serverFound = True
            print(linodeServer.name + " server found")
            break

    if serverFound == False:
        print("Sever " + server + " not found")
        exit(3)

    linodeIp = linodeServer.target

    print("linodeIp: " + linodeIp)
    print("actualIp: " + actualIp)
    if linodeIp == actualIp:
        print("Linode Domain matches actual IP")
    else:
        print("DNS Mismatch! Correcting.")
        linodeServer.target = actualIp
        linodeServer.save()

    serverEntry = serverEntry + 1

exit(0)



