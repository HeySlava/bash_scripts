from __future__ import annotations

import argparse
import json
import os.path
import subprocess

HERE = os.path.dirname(os.path.realpath(__file__))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--remote', default='')
    parser.add_argument('--upstream', default='')
    args = parser.parse_args()

    cmd = (
        os.path.join(HERE, '_git-remote-upstream'),
        '--remote', args.remote, '--upstream', args.upstream,
    )
    remote, upstream = json.loads(subprocess.check_output(cmd))

    if args.dry_run:
        dry_run: tuple[str, ...] = ('echo',)
    else:
        dry_run = ()

    subprocess.check_call(('git', 'fetch', '--all', '--quiet'))

    # if origin/HEAD has never been set, set it automatically
    head_cmd = ('git', 'rev-parse', '--quiet', '--verify', f'{upstream}/HEAD')
    if subprocess.call(head_cmd, stdout=subprocess.DEVNULL):
        set_head_cmd = ('git', 'remote', 'set-head', upstream, '--auto')
        subprocess.check_call(set_head_cmd)

    r_merged_output = subprocess.check_output((
        'git', 'branch', '--remote', '--merged', f'{upstream}/HEAD',
        '--format=%(refname:lstrip=2)',
    ))
    r_merged = [
        line.split('/', 1)[1]
        for line in r_merged_output.decode().splitlines()
        if line.startswith(f'{remote}/')
    ]
    r_merged = [
        branch for branch in r_merged
        if branch not in {'HEAD', 'main', 'master'}
    ]
    if r_merged:
        remote_cmd = (*dry_run, 'git', 'push', remote, '--delete', *r_merged)
        subprocess.check_call(remote_cmd)

    l_merged_output = subprocess.check_output((
        'git', 'branch', '--merged', f'{upstream}/HEAD',
        '--format=%(HEAD)\t%(refname:lstrip=2)',
    ))
    l_merged_info = [
        line.split('\t')
        for line in l_merged_output.decode().splitlines()
    ]
    l_merged = [
        branch for head, branch in l_merged_info
        if head == ' ' and branch not in {'main', 'master'}
    ]
    if l_merged:
        local_cmd = (*dry_run, 'git', 'branch', '--delete', *l_merged)
        subprocess.check_call(local_cmd)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
