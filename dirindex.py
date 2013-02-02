# This script will create or update an index of the contents of a directory
# and store this file inside the directory.

import argparse
import os

def parse_args():
    argparser = argparse.ArgumentParser(description='Index a directory.',
        epilog='''Usage examples: ''')

    argparser.add_argument('-r', '--recursive', action='store_true',
        help=('create the index file(s) by recursing into every directory entries that '
                'are found at deeper levels of the directory structure are indented'))
    argparser.add_argument('-R', '--recurseinto', action='store_true',
        help=('recurse into every directory and create an index file in that directory '
                'containing only the top-level entries'))
    argparser.add_argument('directories', nargs='+', help=('directory or list of '
                            'directories to index'))

    return argparser.parse_args()

def index(dir, recursive):
    if recursive:
        pass # listdir ospathisdir()
    else:
        walk = os.walk(dir).next()
        entries = sorted(
            [entry+'/' for entry in walk[1] if not entry.startswith('.')] +
            [entry for entry in walk[2] if not entry.startswith('.')])
        index = '\n'.join(entries)

    return index

if __name__ == '__main__':
    args = parse_args()
    print index(args.directories[0], True) 
