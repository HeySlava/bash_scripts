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
) -> None:
    p = subprocess.Popen(
            ['xclip', '-selection', 'clipboard', '-o'],
            stdout=subprocess.PIPE,
            text=True,
        )
    message, _ = p.communicate()
    url = HOST + ':' + PORT + '/clipboard/write'
    params = {'password': password, 'message': message}
    print(requests.get(url=url, params=params).json())


def read(
        password: str = _PASSWORD,
) -> None:
    url = HOST + ':' + PORT + '/clipboard/read'
    params = {'password': password,}
    response = requests.get(url=url, params=params)
    message = response.text
    print(response.status_code)

    subprocess.run(['xclip', '-selection', 'clipboard', '-i', '/dev/null'])

    p = subprocess.Popen(
            ['xclip', '-selection', 'clipboard', '-in'],
            stdin=subprocess.PIPE,
            text=True,
        )
    p.communicate(input=message)


def main():
    print("You can't use this module directly")


if __name__ == '__main__':
    main()
