def strip_port(host):
    colon = host.find(':')
    if colon == -1:
        return host
    i = host.find(']')
    if i != -1:
        return host[host.find('(')+1:i]
    return host[:colon]