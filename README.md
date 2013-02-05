dirindex
========

Simple script to create or update a file with an index of a directory.
(index is stored in that directory)

~~~
usage: dirindex.py [-h] [--longhelp] [-r] [-R] [-S SAVEDIR]
                   [directories [directories ...]]

Index a directory.

positional arguments:
  directories           directory or list of directories to index

optional arguments:
  -h, --help            show this help message and exit
  --longhelp            show a help message with usage examples
  -r, --recursive       create the index file(s) by recursing into every
                        directory, entries that are found at deeper levels of
                        the directory structure are indented
  -R, --recurseinto     recurse into every directory in the tree and create an
                        index file in that directory
  -S SAVEDIR, --savedir SAVEDIR
                        store all the index files in the directory specified
                        instead of in the directory they index, the directory
                        must exist

Usage examples:

    this/
        is/
            an/
            example/
                directory
            structure/

    "dirindex.py this/" gives the following index file:
        is/
        EOF

    "dirindex.py -r this/":
        is/
            an/
            example/
                directory
            structure/
        EOF

    These files would be saved as "this.directory_index" under the "this/" directory.
    If you specify --savedir SaveDir, the files would be saved under the "SaveDir/"
    directory.

    "dirindex.py -rR this" would create the following files:
        this/this.directory_index:
            is/
                an/
                example/
                    directory
                structure/
            EOF

        this/is/is.directory_index:
            an/
            example/
                directory
            structure/
            EOF

        this/is/an/an.directory_index:
            EOF

        this/is/example/example.directory_index:
            directory
            EOF

        this/is/structure/structure.directory_index:
            EOF

                    This dirindex.py has Super Chow Powers, so enjoy.
                      Original author: https://github.com/toonn
~~~
