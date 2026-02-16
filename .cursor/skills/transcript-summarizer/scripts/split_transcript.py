#!/usr/bin/env python3
"""
Split a transcript file into chunks of N lines (default 10).
Output: transcript-part1.txt, transcript-part2.txt, ...
"""

import argparse
from pathlib import Path
from typing import List, Optional


def split_transcript(
    input_path: str,
    output_dir: Optional[str] = None,
    chunk_size: int = 10,
    basename: Optional[str] = None,
) -> List[Path]:
    """Split transcript into chunks. Returns list of output file paths."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Transcript not found: {input_path}")

    out_dir = Path(output_dir) if output_dir else path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    base = basename or path.stem

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    output_files = []
    for i in range(0, len(lines), chunk_size):
        chunk = lines[i : i + chunk_size]
        part_num = (i // chunk_size) + 1
        out_path = out_dir / f"{base}-part{part_num}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.writelines(chunk)
        output_files.append(out_path)
        print(f"Wrote {out_path} ({len(chunk)} lines)")

    return output_files


def main():
    parser = argparse.ArgumentParser(description="Split transcript into ~10-line chunks")
    parser.add_argument("transcript", help="Path to transcript file")
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory (default: same as input)",
    )
    parser.add_argument(
        "--chunk-size", "-n",
        type=int,
        default=10,
        help="Lines per chunk (default: 10)",
    )
    parser.add_argument(
        "--basename",
        help="Base name for output files (default: input filename stem)",
    )
    args = parser.parse_args()

    split_transcript(
        args.transcript,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        basename=args.basename,
    )


if __name__ == "__main__":
    main()
