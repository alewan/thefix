#!/usr/bin/env python3
"""Fail if the original project name (or a disguised spelling) appears anywhere.

Usage:
    tools/check_clean.py                 scan file contents and paths
    tools/check_clean.py --message FILE  scan a commit message (commit-msg hook)
    tools/check_clean.py --history       also scan every object and ref in git

Findings are reported as locations only; the offending text is never printed,
so the output of this script is itself safe to keep in logs.

Each pattern is written with a one-character class (for example ``[u]``) so
that the pattern does not match its own source. Add new words the same way.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PATTERNS = [re.compile(p, re.IGNORECASE) for p in (
    r'f[u]ck',                                  # the word itself, any casing
    r'fc[u]k',                                  # transposition typo
    r'f[u]k(?![a-z])',                          # dropped-letter typo
    'аг[с]л',               # typed on a Russian layout
    r'\bw[t]f\b',
)]


def hits(text):
    return any(p.search(text) for p in PATTERNS)


def decode(data):
    return data.decode('utf-8', 'replace')


def git(*args):
    return subprocess.run(('git', '-C', str(REPO)) + args, check=True,
                          capture_output=True).stdout


def in_git_repo():
    return (REPO / '.git').exists()


def list_files():
    """Tracked and untracked-but-not-ignored files, or every file if not a repo."""
    if in_git_repo():
        names = decode(git('ls-files', '-z', '--cached', '--others',
                           '--exclude-standard')).split('\0')
        return sorted(n for n in set(names) if n and (REPO / n).is_file())
    found = []
    for root, dirs, files in os.walk(str(REPO)):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
        found.extend(str(Path(root, f).relative_to(REPO)) for f in files)
    return sorted(found)


def scan_tree():
    problems = []
    for index, name in enumerate(list_files(), 1):
        if hits(name):
            problems.append('file name #{} in sorted listing (not shown)'.format(index))
            continue
        text = decode((REPO / name).read_bytes())
        for number, line in enumerate(text.split('\n'), 1):
            if hits(line):
                problems.append('{}:{}'.format(name, number))
    return problems


def scan_message(path):
    text = decode(Path(path).read_bytes())
    return ['commit message line {}'.format(number)
            for number, line in enumerate(text.split('\n'), 1)
            if not line.startswith('#') and hits(line)]


def scan_history():
    """Every object in the object database (commits, trees, blobs, tags) and
    every ref name. Tree objects hold file names, commit objects hold messages
    and author details, so one pass covers all of them."""
    problems = []
    for ref in decode(git('for-each-ref', '--format=%(refname)')).split('\n'):
        if hits(ref):
            problems.append('a ref name (not shown)')
    stream = git('cat-file', '--batch-all-objects', '--batch')
    position = 0
    while position < len(stream):
        end = stream.index(b'\n', position)
        sha, kind, size = stream[position:end].split()
        body = stream[end + 1:end + 1 + int(size)]
        position = end + 1 + int(size) + 1
        if hits(decode(body)):
            problems.append('git object {} ({})'.format(decode(sha)[:12], decode(kind)))
    return problems


def main(argv):
    args = argv[1:]
    if args[:1] == ['--message'] and len(args) == 2:
        problems, scope = scan_message(args[1]), 'commit message'
    elif args == ['--history']:
        if not in_git_repo():
            sys.exit('check_clean: --history needs a git repository')
        problems, scope = scan_tree() + scan_history(), 'files, paths and git history'
    elif not args:
        problems, scope = scan_tree(), 'files and paths'
    else:
        sys.exit(__doc__)

    if problems:
        print('check_clean: {} blocked occurrence(s) in {}:'.format(len(problems), scope))
        for problem in problems:
            print('  ' + problem)
        return 1
    print('check_clean: clean ({})'.format(scope))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
