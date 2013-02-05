#! /usr/bin/env python

# This script will create or update an index of the contents of a directory
# and store this file inside the directory.

import argparse
import os

class dir:
    space = 4*' '
    def __init__(self, dirname):
        self.name = os.path.basename(os.path.abspath(dirname))
        self.files = []
        self.dirs = []

    def add_files(self, files):
        self.files = files

    def add_dir(self, dir):
        self.dirs.append(dir)

    def __repr__(self):
        repr_string = 'dirname: %s\n'%(self.name)
        repr_string += 'dirs: %s\n'%(', '.join(dirs))
        repr_string += 'files: %s\n'%(', '.join(files))
        return repr_string

    def __str__(self, depth=0):
        dir_strs = [dir.__str__(depth + 1) for dir in self.dirs]
        file_strs = [(depth + 1) * self.space + fil for fil in self.files]
        strs = sorted(dir_strs + file_strs, key=str.lower)
        pretty_dir_string = depth*self.space + self.name + '/'
        for entry in strs:
            pretty_dir_string += '\n' + entry
        return pretty_dir_string


def parse_args():
    class longhelp_print(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            print(parser.format_help() + '\n' + 
                    ('Usage examples:\n'
                    '\n'
                    '    this/\n'
                    '        is/\n'
                    '            an/\n'
                    '            example/\n'
                    '                directory\n'
                    '            structure/\n'
                    '\n'
                    '    "{prog!s} this/" gives the following index file:\n'
                    '        is/\n'
                    '        EOF\n'
                    '\n'
                    '    "{prog!s} -r this/":\n'
                    '        is/\n'
                    '            an/\n'
                    '            example/\n'
                    '                directory\n'
                    '            structure/\n'
                    '        EOF\n'
                    '\n'
                    '    These files would be saved as "this.directory_index" under the '
                    '"this/" directory.\n'
                    '    If you specify --savedir SaveDir, the files would be saved '
                    'under the "SaveDir/"\n    directory.\n'
                    '\n'
                    '    "{prog!s} -rR this" would create the following files:\n'
                    '        this/this.directory_index:\n'
                    '            is/\n'
                    '                an/\n'
                    '                example/\n'
                    '                    directory\n'
                    '                structure/\n'
                    '            EOF\n'
                    '\n'
                    '        this/is/is.directory_index:\n'
                    '            an/\n'
                    '            example/\n'
                    '                directory\n'
                    '            structure/\n'
                    '            EOF\n'
                    '\n'
                    '        this/is/an/an.directory_index:\n'
                    '            EOF\n'
                    '\n'
                    '        this/is/example/example.directory_index:\n'
                    '            directory\n'
                    '            EOF\n'
                    '\n'
                    '        this/is/structure/structure.directory_index:\n'
                    '            EOF\n'
                    '\n'
                    '                    '
                    'This {prog!s} has Super Chow Powers, so enjoy.\n'
                    '                    '
                    '  Original author: https://github.com/toonn'
                    ).format(prog=parser.prog))

    argparser = argparse.ArgumentParser(description='Index a directory.')
    argparser.add_argument('--longhelp', action=longhelp_print, nargs=0,
        help='show a help message with usage examples')
    argparser.add_argument('-r', '--recursive', action='store_true',
        help=('create the index file(s) by recursing into every directory, entries that '
                'are found at deeper levels of the directory structure are indented'))
    argparser.add_argument('-R', '--recurseinto', action='store_true',
        help=('recurse into every directory in the tree and create an index file in that '
                'directory'))
    argparser.add_argument('-S', '--savedir',
        help=('store all the index files in the directory specified instead of in the '
                'directory they index, the directory must exist'))
    argparser.add_argument('directories', nargs='*', help=('directory or list of '
                            'directories to index'))

    return argparser.parse_args()


def index(rootdir):
    # --recursive has the risk of infinite recursion in the os.walk(...) call if there's
    # a link to a parent directory.
    index = ''
    if args.recursive:
        entries = []
        for path, dirs, files in os.walk(rootdir,topdown=False,followlinks=True):
            if not '/.' in path:
                entry = [path, sorted([directory for directory in dirs
                                        if not directory.startswith('.')], key=str.lower),
                            sorted([fil for fil in files if not fil.startswith('.')],
                            key=str.lower)]
                entries.append(entry)
        entries.sort(key=lambda entry : entry[0].lower())

        dirs = {}
        for entry in entries:
            dirname = entry[0]
            directory = dir(dirname)
            directory.add_files(entry[2])
            dirs[dirname] = directory
        for entry in entries:
            # This loop can't be integrated in the previous loop because the dirs
            # dictionary has to be populated first.
            dirname = entry[0]
            for subdir in entry[1]:
                dirs[dirname].add_dir(dirs[os.path.join(dirname,subdir)])
        
        index = dirs[rootdir].__str__() + '\n'

    else:
        walk = os.walk(rootdir).next()
        entries = sorted(
            [entry+'/' for entry in walk[1] if not entry.startswith('.')] +
            [entry for entry in walk[2] if not entry.startswith('.')])
        index = '\n'.join(entries) + '\n'

    return index


def update_index_file(directory):
    # Very inefficient, for --recurseinto because index(rootdir) is called for
    # every directory in the tree, while this could be done all at once since for
    # the __str__ of a higher level directory, the __str__ of a lower level
    # directory is needed.
    if args.savedir is None:
        savedir = os.path.abspath(directory)
    else:
        savedir = os.path.abspath(args.savedir)
    with open(os.path.join(savedir, os.path.basename(os.path.abspath(directory)))
                + '.directory_index', 'w') as index_file:
        index_file.write(index(directory))


if __name__ == '__main__':
    args = parse_args()
    if args.recurseinto:
        all_dirs_in_tree = []
        for directory in args.directories:
            all_dirs_in_tree += [path for path, x, y in
                                    os.walk(directory, followlinks=True)]
        for directory in all_dirs_in_tree:
            update_index_file(directory)
    else:
        for directory in args.directories:
            update_index_file(directory)
