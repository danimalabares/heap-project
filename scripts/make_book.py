#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


def chapter_title(lines, fallback):
    for index, line in enumerate(lines):
        if not line.lstrip().startswith('\\title{'):
            continue
        title_lines = [line]
        while '}' not in title_lines[-1] and index + 1 < len(lines):
            index += 1
            title_lines.append(lines[index])
        title = ''.join(title_lines)
        match = re.search(r'\\title\{(.*?)\}', title, re.S)
        if match:
            return ' '.join(match.group(1).split())
    return fallback.replace('-', ' ').title()


def normalize_title(title):
    return ' '.join(title.split())


def safe_label(text):
    return (
        text.lower()
        .replace('&', 'and')
        .replace('\\', '')
        .replace('{', '')
        .replace('}', '')
        .replace(',', '')
        .replace(':', '')
        .replace('.', '')
        .replace('(', '')
        .replace(')', '')
        .replace('/', '-')
        .replace(' ', '-')
        .replace('--', '-')
    )


def part_label(title):
    return f'part-{safe_label(normalize_title(title))}'


def preamble():
    lines = Path('preamble.tex').read_text(encoding='utf-8').splitlines(True)
    out = [
        '\\documentclass{book}\n',
        '\\usepackage{amsmath}\n',
        '\\usepackage{amssymb}\n',
        '\\usepackage{amsthm}\n',
        '\\newcommand{\\rightlooparrow}{\\mathbin{\\circ\\!\\!\\longrightarrow}}\n',
    ]

    skip_class = False
    skip_external = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('\\IfFileExists{stacks-project.cls}'):
            skip_class = True
            continue
        if skip_class:
            if stripped == '}':
                skip_class = False
            continue
        if skip_external:
            if '}' in line:
                skip_external = False
            continue
        if stripped.startswith('\\externaldocument'):
            if not stripped.rstrip().endswith('}'):
                skip_external = True
            continue
        if stripped.startswith(('\\newcommand', '\\renewcommand', '\\def', '\\DeclareMathOperator')):
            out.append(line)
            continue
        out.append(line)
    return ''.join(out)


def order_entries(order_path):
    if not order_path:
        return []

    path = Path(order_path)
    if not path.exists():
        print(f'warning: order file not found: {order_path}', file=sys.stderr)
        return []

    entries = []
    for line in path.read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        match = re.fullmatch(r'PART\s+[IVXLCDM]+\s*:\s*(.+)', stripped)
        if match:
            entries.append(('part', normalize_title(match.group(1))))
        else:
            entries.append(('chapter', normalize_title(stripped)))
    return entries


def ordered_files(files, order_path):
    if not order_path:
        return files

    entries = [entry for kind, entry in order_entries(order_path) if kind == 'chapter']
    by_title = {}
    for filename in files:
        source = Path(filename)
        if not source.exists():
            continue
        lines = source.read_text(encoding='utf-8').splitlines(True)
        title = normalize_title(chapter_title(lines, source.stem))
        keys = {
            safe_label(title),
            safe_label(source.stem.replace('-', ' ')),
            safe_label(source.stem),
        }
        for key in keys:
            by_title.setdefault(key, filename)

    ordered = []
    used = set()
    for entry in entries:
        key = safe_label(entry)
        filename = by_title.get(key)
        if not filename:
            print(f'warning: no Gerby source matches order-chapters entry: {entry}', file=sys.stderr)
            continue
        if filename in used:
            continue
        ordered.append(filename)
        used.add(filename)

    ordered.extend(filename for filename in files if filename not in used)
    return ordered


def body_for(filename):
    prefix = filename.removesuffix('.tex')
    lines = Path(filename).read_text(encoding='utf-8').splitlines(True)
    title = chapter_title(lines, prefix)
    out = [f'\\chapter{{{title}}}\n', f'\\label{{chapter-{prefix}}}\n\n']

    inside = False
    skipping_title = False
    for line in lines:
        stripped = line.strip()
        if '\\begin{document}' in line:
            inside = True
            continue
        if '\\end{document}' in line:
            break
        if not inside:
            continue
        if skipping_title:
            if '}' in stripped:
                skipping_title = False
            continue
        if stripped.startswith('\\title'):
            if '}' not in stripped:
                skipping_title = True
            continue
        if stripped.startswith('\\maketitle'):
            continue
        if stripped.startswith('\\tableofcontents'):
            continue
        if stripped.startswith('\\phantomsection'):
            continue
        if stripped == '\\label{section-phantom}':
            continue
        if stripped.startswith('\\bibliography'):
            continue
        if stripped.startswith('\\bibliographystyle'):
            continue
        out.append(line)
    return ''.join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--order', help='text file listing chapter titles in TOC order')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    files = ordered_files(args.files, args.order)
    entries = order_entries(args.order)

    print(preamble(), end='')
    print('\\begin{document}\n')
    print('\\tableofcontents\n')
    filenames = iter(files)
    next_filename = next(filenames, None)
    for kind, entry in entries:
        if kind == 'part':
            print(f'\\part{{{entry}}}')
            print(f'\\label{{{part_label(entry)}}}\n')
            continue
        if not next_filename:
            continue
        print(f'% --- Begin {next_filename} ---')
        print(body_for(next_filename), end='')
        print(f'% --- End {next_filename} ---\n')
        next_filename = next(filenames, None)
    while next_filename:
        print(f'% --- Begin {next_filename} ---')
        print(body_for(next_filename), end='')
        print(f'% --- End {next_filename} ---\n')
        next_filename = next(filenames, None)
    print('\\bibliographystyle{amsalpha}')
    print('\\bibliography{my}')
    print('\\end{document}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
