import ipaddress
import socket


class InvalidAccountFormatError(ValueError):
    pass


def parse_account(account_string: str) -> tuple[str, str]:
    if not account_string:
        raise InvalidAccountFormatError

    if account_string.startswith("@"):
        remaining_string = account_string[1:]
        parts = remaining_string.split("@", 1)

        if len(parts) == 2 and parts[0] and parts[1]:
            username = parts[0]
            host = parts[1]
        else:
            raise InvalidAccountFormatError

    else:
        parts = account_string.split("@", 1)

        if len(parts) == 2 and parts[0] and parts[1]:
            username = parts[0]
            host = parts[1]
        else:
            raise InvalidAccountFormatError

    try:
        ip_str = socket.gethostbyname(host)
        ip = ipaddress.ip_address(ip_str)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise InvalidAccountFormatError(
                f"Private address {host} is not allowed"
            )
    except socket.gaierror:
        raise InvalidAccountFormatError(f"Could not resolve host {host}")

    return (username, host)
