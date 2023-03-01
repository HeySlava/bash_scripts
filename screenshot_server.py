#!/usr/bin/python

import argparse
import hashlib
import os
import shlex
import subprocess

from datetime import datetime
from random import random
from pathlib import Path

IMG_SALT = str(random())
IMG_DIR = Path.home() / '.img-bak'
IMG_DIR.mkdir(parents=True, exist_ok=True)
EXTENTION = '.png'
IMG_BASE = 'https://kapitonov.tech/img/'
BACKUP_IMAGE_PATH = 'kapitonov:~/Public/img'


def build_hashed_filename() -> str:
    tmp_filename = IMG_SALT + datetime.now().strftime('%s')
    return hashlib.sha256(tmp_filename.encode()).hexdigest()[:15]


def _get_img_path(filename: str) -> Path:
    final_filename = IMG_DIR / (filename + EXTENTION)
    return final_filename


def _to_clipboard(
        filename: str,
        extention: str = EXTENTION,
        link_base: str = IMG_BASE,
) -> None:
    filename_to_clipboard = link_base + filename + extention
    # TODO: use subprocess instead
    os.system(f'echo -n {filename_to_clipboard} |'
              f'xclip -i -selection clipboard')


def make_screenshot(filename: str) -> None:
    image_path = _get_img_path(filename)
    subprocess.run(shlex.split(f'maim -s {image_path}'))
    subprocess.run(shlex.split(f'scp {image_path} {BACKUP_IMAGE_PATH}'))
    _to_clipboard(filename=filename)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'name',
            nargs='?',
            metavar='NAME',
            help='Type your filename without extention. Default sha256',
        )

    args = parser.parse_args()

    if args.name:
        filename = args.name
    else:
        filename = build_hashed_filename()
    make_screenshot(filename=filename)
    return 0


if __name__ == '__main__':
    main()
