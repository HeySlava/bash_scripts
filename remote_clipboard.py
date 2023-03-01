import subprocess
from typing import Dict
from pathlib import Path

import requests

HOST = 'https://kapitonov.tech'
PORT = '443'

content = (Path(__file__).parent / '.env').read_text()
_PASSWORD = content.partition('=')[-1].strip()
if not _PASSWORD:
    raise ValueError('Password is not inited. Put it hire in .env')


def write(
        password: str = _PASSWORD,
) -> Dict[str, str]:
    p = subprocess.Popen(
            ['xclip', '-selection', 'clipboard', '-o'],
            stdout=subprocess.PIPE,
            text=True,
        )
    message, _ = p.communicate()
    url = HOST + ':' + PORT + '/clipboard/write'
    params = {'password': password, 'message': message}
    return requests.get(url=url, params=params).json()


def read(
        password: str = _PASSWORD,
) -> str:
    p = subprocess.Popen(
            ['xclip', '-selection', 'clipboard', '-o'],
            stdin=subprocess.PIPE,
        )

    url = HOST + ':' + PORT + '/clipboard/read'
    params = {'password': password,}
    message = requests.get(url=url, params=params).content
    p.communicate(input=message)
    return message.decode('utf-8')


def main():
    print("You can't use this module directly")


if __name__ == '__main__':
    main()
