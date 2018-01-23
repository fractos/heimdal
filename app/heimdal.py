import os
import quickproxy
import json
import socket,struct
import settings
from logzero import logger

def callback(request):
    request.host = settings.TARGET_HOST
    request.port = settings.TARGET_PORT

    first_remote_ip = '0.0.0.0'

    if request.headers.get('X-Forwarded-For'):
        first_remote_ip = request.headers['X-Forwarded-For'].split(", ")[0]

    logger.debug('request received: (' + first_remote_ip + ') ' + request.method + ' ' + request.path)

    allowed = ip_passes(first_remote_ip, request.method)

    if allowed:
        logger.info('allowed ' + request.method + ' request from ' + first_remote_ip)
        return request

    logger.info('denied ' + request.method + ' request from ' + first_remote_ip)

    return quickproxy.ResponseObj(
        code=403,
        body='')

def address_in_network(ip, net_n_bits):
    ''' from https://stackoverflow.com/a/30676234 '''
    ipaddr = struct.unpack('!L', socket.inet_aton(ip))[0]
    net, bits = net_n_bits.split('/')
    netaddr = struct.unpack('!L', socket.inet_aton(net))[0]
    netmask = (0xFFFFFFFF >> int(bits)) ^ 0xFFFFFFFF
    return ipaddr & netmask == netaddr

def ip_passes(test_ip, test_method):
    for rule in rules['rules']:
        for method in rule['methods']:
            if method == test_method:
                for source in rule['source']:
                    if address_in_network(test_ip, source):
                        return rule['effect'] == 'ALLOW' and True
    return False

rules = json.loads(open(settings.RULES_FILE).read())

quickproxy.run_proxy(port=settings.LISTENER_PORT, req_callback=callback)
