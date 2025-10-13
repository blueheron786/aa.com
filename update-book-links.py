#!/usr/bin/env python3
"""
Update book markdown files with retailer links from book-links.json

Matches books by slug or filename, then updates frontmatter with:
- buy_paperback_<retailer>: <url>
- buy_ebook_<retailer>: <url>

Preserves existing frontmatter and content.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional


def parse_frontmatter(content: str) -> tuple[Dict[str, str], str, str]:
    """
    Parse YAML frontmatter from markdown content.
    
    Returns:
        (frontmatter_dict, body_content, original_frontmatter_text)
    """
    # Check for fenced YAML (---...---)
    fenced_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    
    if fenced_match:
        yaml_content = fenced_match.group(1)
        body_content = fenced_match.group(2)
        
        # Parse YAML into dict
        frontmatter = {}
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                frontmatter[key] = value
        
        return frontmatter, body_content, yaml_content
    
    return {}, content, ""


def sanitize_retailer_name(retailer: str) -> str:
    """
    Convert retailer name to valid frontmatter key.
    
    Examples:
        "Barnes & Noble" -> "barnes_noble"
        "Bookshop.org" -> "bookshop_org"
        "Amazon" -> "amazon"
    """
    # Lowercase, replace special chars with underscore
    sanitized = retailer.lower()
    sanitized = re.sub(r'[^a-z0-9]+', '_', sanitized)
    sanitized = sanitized.strip('_')
    return sanitized


def build_frontmatter_text(frontmatter: Dict[str, str]) -> str:
    """
    Build YAML frontmatter text from dictionary.
    Preserves order for readability.
    """
    # Define order for common fields
    field_order = [
        'title', 'datePublished', 'category', 'template', 'slug',
        'summary', 'cover', 'buy_link'
    ]
    
    lines = []
    
    # Add ordered fields first
    for field in field_order:
        if field in frontmatter:
            lines.append(f"{field}: {frontmatter[field]}")
    
    # Add buy_paperback_* fields
    paperback_fields = sorted([k for k in frontmatter.keys() if k.startswith('buy_paperback_')])
    if paperback_fields:
        lines.append("")  # Blank line for readability
        lines.append("# Paperback retailers")
        for field in paperback_fields:
            lines.append(f"{field}: {frontmatter[field]}")
    
    # Add buy_ebook_* fields
    ebook_fields = sorted([k for k in frontmatter.keys() if k.startswith('buy_ebook_')])
    if ebook_fields:
        lines.append("")  # Blank line for readability
        lines.append("# eBook retailers")
        for field in ebook_fields:
            lines.append(f"{field}: {frontmatter[field]}")
    
    # Add any remaining fields
    added_fields = set(field_order + paperback_fields + ebook_fields)
    remaining_fields = sorted([k for k in frontmatter.keys() if k not in added_fields])
    for field in remaining_fields:
        lines.append(f"{field}: {frontmatter[field]}")
    
    return '\n'.join(lines)


def update_book_file(book_path: Path, book_slug: str, book_data: Dict[str, Any]) -> bool:
    """
    Update a book markdown file with retailer links.
    
    Args:
        book_path: Path to the markdown file
        book_slug: Slug identifier for the book
        book_data: Dictionary containing 'paperback' and/or 'ebook' retailer links
    
    Returns:
        True if file was updated, False otherwise
    """
    # Read current content
    content = book_path.read_text(encoding='utf-8')
    frontmatter, body, _ = parse_frontmatter(content)
    
    # Verify this is the right book (check slug matches)
    if frontmatter.get('slug') != book_slug:
        # Also try matching by filename
        filename_slug = book_path.stem  # filename without extension
        if filename_slug != book_slug:
            return False
    
    updated = False
    
    # Add paperback links
    if 'paperback' in book_data:
        for retailer, url in book_data['paperback'].items():
            field_name = f"buy_paperback_{sanitize_retailer_name(retailer)}"
            if frontmatter.get(field_name) != url:
                frontmatter[field_name] = url
                updated = True
    
    # Add ebook links
    if 'ebook' in book_data:
        for retailer, url in book_data['ebook'].items():
            field_name = f"buy_ebook_{sanitize_retailer_name(retailer)}"
            if frontmatter.get(field_name) != url:
                frontmatter[field_name] = url
                updated = True
    
    if not updated:
        return False
    
    # Rebuild the file
    new_frontmatter = build_frontmatter_text(frontmatter)
    new_content = f"---\n{new_frontmatter}\n---\n\n{body}"
    
    # Write back to file
    book_path.write_text(new_content, encoding='utf-8')
    return True


def main():
    """Main entry point."""
    # Load book links data
    links_file = Path(__file__).parent / 'content' / 'book-links.json'
    books_dir = Path(__file__).parent / 'content' / 'books'
    
    if not links_file.exists():
        print(f"❌ Error: {links_file} not found")
        return 1
    
    if not books_dir.exists():
        print(f"❌ Error: {books_dir} not found")
        return 1
    
    # Load JSON data
    with open(links_file, 'r', encoding='utf-8') as f:
        book_links = json.load(f)
    
    print(f"📚 Found {len(book_links)} books in book-links.json")
    print(f"📂 Scanning {books_dir} for markdown files...\n")
    
    # Process each book
    updated_count = 0
    skipped_count = 0
    
    for book_slug, book_data in book_links.items():
        print(f"Processing: {book_slug}")
        
        # Try to find matching markdown file
        # First try exact filename match
        book_file = books_dir / f"{book_slug}.md"
        
        if not book_file.exists():
            # Try finding by slug in frontmatter
            found = False
            for md_file in books_dir.glob("*.md"):
                content = md_file.read_text(encoding='utf-8')
                frontmatter, _, _ = parse_frontmatter(content)
                if frontmatter.get('slug') == book_slug:
                    book_file = md_file
                    found = True
                    break
            
            if not found:
                print(f"  ⚠️  No matching markdown file found for '{book_slug}'")
                skipped_count += 1
                continue
        
        # Update the file
        if update_book_file(book_file, book_slug, book_data):
            paperback_count = len(book_data.get('paperback', {}))
            ebook_count = len(book_data.get('ebook', {}))
            print(f"  ✅ Updated {book_file.name}")
            print(f"     Added {paperback_count} paperback + {ebook_count} ebook links")
            updated_count += 1
        else:
            print(f"  ℹ️  No changes needed for {book_file.name}")
            skipped_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✨ Complete!")
    print(f"   Updated: {updated_count} books")
    print(f"   Skipped: {skipped_count} books (no changes or not found)")
    print(f"{'='*60}")
    
    return 0


if __name__ == '__main__':
    exit(main())
