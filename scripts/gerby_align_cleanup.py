#!/usr/bin/env python3

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    "_site",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    "tmp",
    "gerby",
}

VERBATIM_ENVS = {"verbatim", "lstlisting", "minted", "Verbatim"}

BEGIN_ALIGN = r"\begin{align*}"
END_ALIGN = r"\end{align*}"


@dataclass
class Block:
    start_line: int
    end_line: int
    lines: list[str]
    suspicious: bool


def is_commented(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("%")


def env_name_from_begin(line: str) -> str | None:
    m = re.search(r"\\begin\{([A-Za-z*]+)\}", line)
    return m.group(1) if m else None


def env_name_from_end(line: str) -> str | None:
    m = re.search(r"\\end\{([A-Za-z*]+)\}", line)
    return m.group(1) if m else None


def normalize_angle_delims(text: str) -> str:
    text = text.replace(r"\left<", r"\left\langle{}")
    text = text.replace(r"\right>", r"\right\rangle{}")
    text = re.sub(r"\\left\\langle(?!\{\})", r"\\left\\langle{}", text)
    text = re.sub(r"\\right\\rangle(?!\{\})", r"\\right\\rangle{}", text)
    return text


def scan_tex_file(path: Path) -> tuple[list[Block], int, int]:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    blocks: list[Block] = []
    in_verbatim: str | None = None
    i = 0
    left_count = 0
    right_count = 0
    while i < len(lines):
        line = lines[i]
        if in_verbatim:
            if not is_commented(line):
                end_env = env_name_from_end(line)
                if end_env == in_verbatim:
                    in_verbatim = None
            i += 1
            continue
        if not is_commented(line):
            begin_env = env_name_from_begin(line)
            if begin_env in VERBATIM_ENVS:
                in_verbatim = begin_env
                i += 1
                continue
        if not is_commented(line):
            left_count += line.count(r"\left<") + line.count(r"\left\langle")
            right_count += line.count(r"\right>") + line.count(r"\right\rangle")
        if is_commented(line):
            i += 1
            continue
        if BEGIN_ALIGN in line:
            start = i
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if not is_commented(lines[i]) and END_ALIGN in lines[i]:
                    break
                i += 1
            suspicious = any(
                token in "".join(block)
                for token in (
                    r"\intertext",
                    r"\shortintertext",
                    r"\tag",
                    r"\label",
                    r"\nonumber",
                    r"\notag",
                )
            ) or any(
                re.search(r"\\(begin|end)\{(?!align\*\})[^}]+\}", l)
                for l in block
                if not is_commented(l)
            )
            blocks.append(Block(start + 1, i + 1, block, suspicious))
        i += 1
    return blocks, left_count, right_count


def replace_simple_blocks(text: str) -> tuple[str, int, list[Block]]:
    lines = text.splitlines(True)
    out: list[str] = []
    in_verbatim: str | None = None
    i = 0
    converted = 0
    suspicious_blocks: list[Block] = []

    while i < len(lines):
        line = lines[i]
        if in_verbatim:
            out.append(line)
            if not is_commented(line) and env_name_from_end(line) == in_verbatim:
                in_verbatim = None
            i += 1
            continue

        if not is_commented(line):
            begin_env = env_name_from_begin(line)
            if begin_env in VERBATIM_ENVS:
                in_verbatim = begin_env
                out.append(line)
                i += 1
                continue

        if is_commented(line):
            out.append(line)
            i += 1
            continue

        if BEGIN_ALIGN not in line:
            line = normalize_angle_delims(line)
            out.append(line)
            i += 1
            continue

        start = i
        block = [line]
        i += 1
        while i < len(lines):
            block.append(lines[i])
            if not is_commented(lines[i]) and END_ALIGN in lines[i]:
                break
            i += 1

        block_text = "".join(block)
        suspicious = any(
            token in block_text
            for token in (
                r"\intertext",
                r"\shortintertext",
                r"\tag",
                r"\label",
                r"\nonumber",
                r"\notag",
            )
        ) or any(
            re.search(r"\\(begin|end)\{(?!align\*\})[^}]+\}", l)
            for l in block
            if not is_commented(l)
        )
        if suspicious:
            suspicious_blocks.append(Block(start + 1, i + 1, block, True))
            for l in block:
                out.append(normalize_angle_delims(l))
            i += 1
            continue

        if len(block) == 1:
            single = block[0].replace(BEGIN_ALIGN, "$$\n\\begin{aligned}")
            single = single.replace(END_ALIGN, "\\end{aligned}\n$$")
            out.append(normalize_angle_delims(single))
        else:
            first = block[0].replace(BEGIN_ALIGN, "$$\n\\begin{aligned}")
            last = block[-1].replace(END_ALIGN, "\\end{aligned}\n$$")
            out.append(normalize_angle_delims(first))
            for mid in block[1:-1]:
                out.append(normalize_angle_delims(mid))
            out.append(normalize_angle_delims(last))
        converted += 1
        i += 1
    return "".join(out), converted, suspicious_blocks


def iter_tex_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".tex"):
                files.append(Path(dirpath) / filename)
    return sorted(files)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    changed_files = 0
    converted_blocks = 0
    left_replacements = 0
    right_replacements = 0
    suspicious_all: list[tuple[Path, Block]] = []

    for path in iter_tex_files(root):
        original = path.read_text(encoding="utf-8")
        blocks, left_hits, right_hits = scan_tex_file(path)
        updated, converted, suspicious = replace_simple_blocks(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
        converted_blocks += converted
        left_replacements += left_hits
        right_replacements += right_hits
        for block in suspicious:
            suspicious_all.append((path, block))
        for block in blocks:
            if block.suspicious:
                suspicious_all.append((path, block))

    print(f"Changed files: {changed_files}")
    print(f"Converted align* blocks: {converted_blocks}")
    print(f"Left replacements: {left_replacements}")
    print(f"Right replacements: {right_replacements}")
    if suspicious_all:
        print("Suspicious align* blocks left unchanged:")
        seen = set()
        for path, block in suspicious_all:
            key = (path, block.start_line, block.end_line)
            if key in seen:
                continue
            seen.add(key)
            print(f"- {path.relative_to(root)}:{block.start_line}-{block.end_line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
