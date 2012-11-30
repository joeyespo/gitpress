import os
import re


def preview(working_directory='.', host=None, port=None):
    """Runs a local server to preview the working directory of a repository."""
    # TODO: implement
    return


def parse_address(address):
    """Returns (host, port) from the specified address."""
    # TODO: implement
    host = address
    port = None
    return host, port


def resolve_address(path_or_address, address=None):
    """Returns (path, address) based on two optional arguments [path] [address]."""
    if path_or_address is None or address is not None:
        return path_or_address, address

    path = None
    if not valid_address(path_or_address) or os.path.exists(path_or_address):
        path = path_or_address
    else:
        address = path_or_address

    return path, address


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
