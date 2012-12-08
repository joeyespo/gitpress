import re


def valid_address(address):
    """Determines whether the specified address string is valid."""
    if not address:
        return False

    components = address.split(':')
    if len(components) > 2 or not valid_hostname(components[0]):
        return False

    if len(components) == 2 and not valid_port(components[1]):
        return False

    return True


def valid_hostname(host):
    """Returns whether the specified string is a valid hostname."""
    if len(host) > 255:
        return False
    if host[-1:] == '.':
        host = host[:-1]
    allowed = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
    return all(allowed.match(x) for x in host.split('.'))


def valid_port(port):
    """Returns whether the specified string is a valid port."""
    try:
        return 1 <= int(port) <= 65535
    except:
        return False
