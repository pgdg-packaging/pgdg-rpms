#!/usr/bin/env python3
#
# mock-ci-matrix.py [--base origin/master] [--mock-dir /etc/mock] [pkg ...]
#
# Print the GitHub Actions build matrix (JSON) for the packages changed
# between --base and HEAD, or for the packages given on the command line.
#
# Which OSes and PostgreSQL versions a package is built for comes from the
# repo layout, the same way mock-build-matrix.sh decides it:
#   - OS dirs next to main/ (F-44, EL-9, SLES-16, AL-2023, ...)
#   - rpm/redhat/<PG>/<pkg> entries, for non-common and non-free packages
#   - a pgdg-<distro>-pg<PG>-x86_64.cfg mock config must exist as well
#
# SLES-15 is left out: Leap 15.6 is EOL and there is no Leap 15.7 to stand
# in for SLES 15 SP7.
#
# common and extras packages are not PG specific: every OS, against PG 18.
# non-common and non-free packages: every supported PG version on Rocky 8
# (Rocky 9 when there is no EL-8) and Fedora 44, plus every OS at the newest
# stable PG version the package supports there.
#
# Per https://github.com/pgdg-packaging/pgdg-rpms/issues/442

import argparse
import json
import os
import re
import subprocess
import sys

REPO_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                           capture_output=True, text=True,
                           check=True).stdout.strip()
REDHAT = os.path.join(REPO_ROOT, 'rpm', 'redhat')
MAIN = os.path.join(REDHAT, 'main')
KINDS = ('common', 'non-common', 'non-free', 'extras')

DISTRO_MARKER = {
    'fedora-43': 'F-43',
    'fedora-44': 'F-44',
    'fedora-45': 'F-45',
    'rocky-8': 'EL-8',
    'rocky-9': 'EL-9',
    'rocky-10': 'EL-10',
    'opensuse-leap-16': 'SLES-16',
    'amazonlinux-2023': 'AL-2023',
}

COMMON_PG = '18'

def stable_pg_versions():
    path = os.path.join(REPO_ROOT, 'scripts', 'buildserver', 'global.sh')
    with open(path) as f:
        m = re.search(r'^declare -a pgStableBuilds=\(([^)]*)\)', f.read(), re.M)
    return set(m.group(1).split())


def find_kind(pkg):
    for kind in KINDS:
        if os.path.isdir(os.path.join(MAIN, kind, pkg, 'main')):
            return kind
    return None


def changed_packages(base):
    out = subprocess.run(['git', 'diff', '--name-only', f'{base}...HEAD'],
                         capture_output=True, text=True, check=True).stdout
    pkgs = set()
    for path in out.splitlines():
        parts = path.split('/')
        if parts[:3] == ['rpm', 'redhat', 'main'] and len(parts) > 5 \
                and parts[3] in KINDS:
            pkgs.add(parts[4])
        elif parts[:2] == ['rpm', 'redhat'] and len(parts) > 3 \
                and parts[2].isdigit():
            pkgs.add(parts[3])
    return sorted(pkgs)


def matrix_for(pkg, configs, stable):
    kind = find_kind(pkg)
    if kind is None:
        print(f'{pkg}: not found under rpm/redhat/main, skipping',
              file=sys.stderr)
        return []
    root = os.path.join(MAIN, kind, pkg)
    if os.path.exists(os.path.join(root, 'main', 'dead.package')):
        return []
    distros = [d for d, m in DISTRO_MARKER.items()
               if os.path.isdir(os.path.join(root, m))]

    def buildable(distro, pg):
        return (distro, pg) in configs

    if kind in ('common', 'extras'):
        jobs = {(d, COMMON_PG) for d in distros if buildable(d, COMMON_PG)}
    else:
        pgs = sorted((v for v in os.listdir(REDHAT) if v.isdigit()
                      and os.path.isdir(os.path.join(REDHAT, v, pkg))),
                     key=int)
        jobs = set()
        sweep = ['rocky-8' if 'rocky-8' in distros else 'rocky-9', 'fedora-44']
        for d in sweep:
            if d in distros:
                jobs |= {(d, pg) for pg in pgs if buildable(d, pg)}
        for d in distros:
            ok = [pg for pg in pgs if pg in stable and buildable(d, pg)]
            if ok:
                jobs.add((d, ok[-1]))

    return [{'package': pkg, 'kind': kind, 'distro': d, 'pg': pg,
             'osdir': DISTRO_MARKER[d]}
            for d, pg in sorted(jobs, key=lambda j: (j[0], int(j[1])))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='origin/master')
    ap.add_argument('--mock-dir', default='/etc/mock')
    ap.add_argument('packages', nargs='*')
    args = ap.parse_args()

    configs = set()
    for f in os.listdir(args.mock_dir):
        m = re.match(r'pgdg-(.+)-pg(\d+)-x86_64\.cfg$', f)
        if m:
            configs.add((m.group(1), m.group(2)))

    pkgs = args.packages or changed_packages(args.base)
    stable = stable_pg_versions()
    include = [job for pkg in pkgs for job in matrix_for(pkg, configs, stable)]
    print(json.dumps({'include': include}))


if __name__ == '__main__':
    main()
