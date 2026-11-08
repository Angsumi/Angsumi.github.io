import argparse
import getpass
import json
import os
from .lead_store import Store
from .server import password_hash
from .notifications import deliver, schedule


def main():
    parser=argparse.ArgumentParser(description='ANGSUMI owner operations. Secrets never belong in command arguments.')
    parser.add_argument('command',choices=['hash-password','deliver','schedule','backup'])
    parser.add_argument('--destination')
    args=parser.parse_args()
    if args.command=='hash-password':
        password=getpass.getpass('New owner password (at least 16 characters): ')
        if len(password)<16:
            parser.error('Use at least 16 characters')
        print(password_hash(password))
        return
    path=os.environ.get('LEAD_DB_PATH')
    if not path:
        parser.error('LEAD_DB_PATH is required')
    store=Store(path)
    if args.command=='deliver':
        print(json.dumps(deliver(store)))
    elif args.command=='schedule':
        print(json.dumps({'scheduled':schedule(store)}))
    elif args.command=='backup':
        if not args.destination:
            parser.error('--destination is required')
        store.backup(args.destination)
        print('Private SQLite backup completed')


if __name__=='__main__':
    main()
