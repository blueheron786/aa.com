#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

BASE_AA = Path("/srv/shared/code/aa.com")
BASE_MM = Path("/srv/shared/code/mm")
BOOKS_DIR_AA = BASE_AA / "content" / "books"
BOOKS_DIR_MM = BASE_MM / "content" / "books"

EXCEPTION_REL = Path("2023/facts-about-palestine.md")


def sync_book_files():
    """Sync book Markdown files between aa.com and mm.
    - Prefer aa.com content when both exist.
    - Do NOT copy exception file from mm to aa.com.
    - Copy missing files from whichever side has them.
    """
    # Collect all relative paths from both sides
    all_rel = set()
    for base in (BOOKS_DIR_AA, BOOKS_DIR_MM):
        for p in base.rglob("*.md"):
            if p.name == "_index.md":
                continue
            all_rel.add(p.relative_to(base))

    for rel in sorted(all_rel):
        aa_file = BOOKS_DIR_AA / rel
        mm_file = BOOKS_DIR_MM / rel

        if aa_file.exists() and mm_file.exists():
            # both exist: copy aa.com to mm (aa has more fields)
            shutil.copy2(aa_file, mm_file)
            print(f"Merged {rel} (aa.com -> mm)")
        elif aa_file.exists():
            # only in aa.com: copy to mm
            shutil.copy2(aa_file, mm_file)
            print(f"Copied {rel} (aa.com -> mm)")
        elif mm_file.exists():
            # only in mm
            if rel == EXCEPTION_REL:
                # do not copy exception to aa.com
                print(f"Skipping {rel} (keeping only in mm)")
            else:
                shutil.copy2(mm_file, aa_file)
                print(f"Copied {rel} (mm -> aa.com)")
        else:
            print(f"Warning: {rel} not found in either")


def generate_index(base: Path):
    """Generate _index.md for given base (aa.com or mm)."""
    index_file = base / "content" / "books" / "_index.md"
    # Gather markdown files, optionally skip exception for aa.com
    files = []
    for p in (base / "content" / "books").rglob("*.md"):
        if p.name == "_index.md":
            continue
        rel = p.relative_to(base / "content" / "books")
        if base == BASE_AA and rel == EXCEPTION_REL:
            continue
        files.append(p)
    files.sort()

    lines = [
        "---",
        "title: Books",
        "---",
        "",
        "# Books",
        "",
    ]
    for f in files:
        rel = f.relative_to(base / "content" / "books")
        link_path = f"/books/{rel.with_suffix('')}/"
        # extract title from frontmatter
        title = None
        try:
            with open(f, 'r') as fp:
                for line in fp:
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                        break
        except Exception:
            pass
        if not title:
            title = f.stem.replace("-", " ").title()
        lines.append(f"- [{title}]({link_path})")
    lines.append("")  # trailing newline

    index_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {index_file}")


def main():
    sync_book_files()
    generate_index(BASE_AA)
    generate_index(BASE_MM)
    print("Done.")


if __name__ == "__main__":
    main()