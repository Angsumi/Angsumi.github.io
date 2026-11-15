"""Notify IndexNow (Bing, Yandex, Seznam, Naver; Bing's index feeds ChatGPT and Copilot search) of sitemap URLs.

Usage: python3 scripts/indexnow.py [--dry-run]
The key file 6c3d5fd49dcb41b5ac4b7e3a74b7c048.txt is served from the site root.
"""
from pathlib import Path
from xml.etree import ElementTree
import json
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
HOST = 'angsumi.online'
KEY = '6c3d5fd49dcb41b5ac4b7e3a74b7c048'


def sitemap_urls():
    tree = ElementTree.parse(ROOT / 'sitemap.xml')
    return [loc.text for loc in tree.findall('.//{*}loc')] + [f'https://{HOST}/llms.txt']


def payload():
    assert (ROOT / f'{KEY}.txt').read_text().strip() == KEY, 'IndexNow key file mismatch'
    return {'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': sitemap_urls()}


def main(dry_run=False):
    body = payload()
    if dry_run:
        print(json.dumps(body, indent=2))
        return
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f'IndexNow: HTTP {resp.status} for {len(body["urlList"])} URLs')
    except urllib.error.HTTPError as err:
        # 202 = accepted pending key check; 4xx is reported but never fails a deploy that already succeeded.
        print(f'IndexNow: HTTP {err.code} {err.read()[:200]!r}')


if __name__ == '__main__':
    main('--dry-run' in sys.argv)
