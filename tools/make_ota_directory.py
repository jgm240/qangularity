#!/usr/bin/env python3
"""Builds ota/directory.json, the file qAngularity reads to find Angularity FW updates.

The format is the one the upstream Flipper mobile apps already understand
(same JSON as https://update.flipperzero.one/firmware/directory.json), so the
app's whole download -> verify -> push-to-Flipper pipeline is unchanged.

Usage (after attaching the .tgz to a GitHub release with the same tag):

    python3 tools/make_ota_directory.py \\
        --tgz "/Users/me/Desktop/Angularity FW/AngularityFW-release25.tgz" \\
        --tag AngularityFW-release25 \\
        --changelog "Pseudo-Off mode, theft alarm lockout fixes" \\
        --out /path/to/angularity-fw/ota/directory.json

Existing entries in --out are kept, so running this once per release builds up
the version history. The newest timestamp wins on the phone.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

REPO = 'jgm240/angularity-fw'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tgz', required=True, type=Path, help='updater package (flipper-z-f7-update-*.tgz)')
    ap.add_argument('--tag', required=True, help='GitHub release tag the .tgz is attached to')
    ap.add_argument('--changelog', default='', help='shown in the app before updating')
    ap.add_argument('--channel', default='release', choices=['release', 'release-candidate', 'development'])
    ap.add_argument('--asset-name', help='file name on the release (default: the .tgz basename)')
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()

    asset = args.asset_name or args.tgz.name
    entry = {
        'version': args.tag,
        'changelog': args.changelog,
        'timestamp': int(time.time()),
        'files': [{
            'url': f'https://github.com/{REPO}/releases/download/{args.tag}/{asset.replace(" ", "%20")}',
            'target': 'f7',
            'type': 'update_tgz',
            'sha256': sha256(args.tgz),
        }],
    }

    titles = {
        'release': ('Release', 'Stable Angularity FW builds'),
        'release-candidate': ('Release Candidate', 'Pre-release Angularity FW builds'),
        'development': ('Development', 'Unstable Angularity FW builds'),
    }

    doc = {'channels': []}
    if args.out.exists():
        doc = json.loads(args.out.read_text())

    channel = next((c for c in doc['channels'] if c['id'] == args.channel), None)
    if channel is None:
        title, desc = titles[args.channel]
        channel = {'id': args.channel, 'title': title, 'description': desc, 'versions': []}
        doc['channels'].append(channel)

    channel['versions'] = [v for v in channel['versions'] if v['version'] != args.tag] + [entry]
    channel['versions'].sort(key=lambda v: v['timestamp'], reverse=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2) + '\n')
    print(f'wrote {args.out}: {args.tag} sha256={entry["files"][0]["sha256"]}')


if __name__ == '__main__':
    main()
