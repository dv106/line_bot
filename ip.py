import netifaces as ni

ni.ifaddresses('enp0s8')
ip = ni.ifaddresses('enp0s8')[ni.AF_INET][0]['addr']
print(ip)