#!/usr/bin/env python
# -*- python -*-

# MIT License
# Copyright (c) 2017 Contact Software

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""globcopy copies subtrees described by glob patterns, supporting
recursive wildcards. The patter"""

import os
import sys
import argparse
import shutil
import glob2


class Usage(Exception):
    pass


def prep_path(p):
    return os.path.normpath(os.path.expanduser(os.path.expandvars(p)))


def globcopy(base, prefix, patterns, verbose=False, dry_run=False):
    """Do the actual work here, i.e. copying files, creating directories
    etc. If `verbose`, print what is (or would be) done. If `dry_run`
    do not change the filesystem at all."""
    if verbose:
        def say(msg): sys.stdout.write("%s\n" % msg)
    else:
        def say(msg): pass

    expanded_base = prep_path(base)

    expanded_prefix = prep_path(prefix)
    if not os.path.exists(expanded_prefix):
        raise Usage("Target prefix '%s' does not exist" % expanded_prefix)

    # Memorize created directories to avoid repeated "mkdir ..."
    # message for verbose==True
    dirs_created = set()

    for pattern in patterns:
        pattern = prep_path(os.path.join(expanded_base, pattern))
        for fn in glob2.iglob(pattern):
            relfn = fn[len(expanded_base)+len(os.sep):]
            reldir = os.path.dirname(relfn)
            targetdir = os.path.join(expanded_prefix, reldir)
            if not (os.path.exists(targetdir) or targetdir in dirs_created):
                say("mkdir %s" % os.path.join(prefix, reldir))
                dirs_created.add(targetdir)
                if not dry_run:
                    os.makedirs(targetdir)
            if os.path.isfile(fn):
                say("cp %s %s" % (os.path.join(base, relfn),
                                  os.path.join(prefix, reldir)))
                if not dry_run:
                    shutil.copy(fn, targetdir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-n", "--dry-run", action="store_true")
    parser.add_argument("base",
                        help="""
                        The source directory from which trees are copied.""")
    parser.add_argument("prefix",
                        help="""
                        The destination directory. New subdirectories are
                        created if necessary.""")
    parser.add_argument("patterns", nargs="+",
                        help="""
                        Each pattern argument describes a partial subtree using
                        a glob-style syntax. Recursive wildcards are supported.
                        """)
    args = parser.parse_args()
    try:
        globcopy(args.base, args.prefix, args.patterns,
                 verbose=args.verbose, dry_run=args.dry_run)
    except Usage as u:
        sys.stderr.write("globcopy: %s\n" % u)
        return -1


if __name__ == "__name__":
    sys.exit(main())
