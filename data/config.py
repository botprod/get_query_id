# api id, hash
API_ID = 1234
API_HASH = 'botprod!'

DELAYS = {
    "ACCOUNT": [10, 15],
    "RELOGIN": [5, 7],  # delay after a login attempt
}

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": "socks5",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "socks5"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
    }
}

# session folder (do not change)
WORKDIR = "sessions/"
JSON_WORKDIR = "output/"
# timeout in seconds for checking accounts on valid
TIMEOUT = 30
