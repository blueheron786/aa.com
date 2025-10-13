# Book Links Update Script

## Overview

The `update-book-links.py` script automatically updates book markdown files with retailer links from `content/book-links.json`.

## Architecture

### Data Structure

**book-links.json** stores retailer links by book slug:

```json
{
    "book-slug-here": {
        "paperback": {
            "Amazon": "https://...",
            "Barnes & Noble": "https://..."
        },
        "ebook": {
            "Kobo": "https://...",
            "Apple": "https://..."
        }
    }
}
```

### Frontmatter Fields

The script adds these fields to your book markdown files:

- `buy_paperback_<retailer>` - Paperback buy links
- `buy_ebook_<retailer>` - eBook buy links

Retailer names are sanitized: `"Barnes & Noble"` → `buy_ebook_barnes_noble`

### Matching Logic

Books are matched by:
1. **Filename**: `the-green-beast.md` matches slug `"the-green-beast"`
2. **Frontmatter slug**: Falls back to checking the `slug` field in frontmatter

## Usage

1. **Add links to book-links.json**:
   ```json
   {
       "the-green-beast": {
           "paperback": {
               "Amazon": "https://amazon.com/...",
               "Walmart": "https://walmart.com/..."
           },
           "ebook": {
               "Kobo": "https://kobo.com/..."
           }
       }
   }
   ```

2. **Run the script**:
   ```bash
   python update-book-links.py
   ```

3. **Result in markdown**:
   ```markdown
   ---
   title: The Green Beast
   slug: the-green-beast
   buy_link: https://books2read.com/greenbeast
   
   # Paperback retailers
   buy_paperback_amazon: https://amazon.com/...
   buy_paperback_walmart: https://walmart.com/...
   
   # eBook retailers
   buy_ebook_kobo: https://kobo.com/...
   ---
   ```

## Features

✅ **Preserves existing frontmatter** - Won't overwrite other fields  
✅ **Idempotent** - Safe to run multiple times  
✅ **Organized output** - Groups paperback/ebook links with comments  
✅ **Smart matching** - Matches by filename or slug field  
✅ **Detailed logging** - Shows exactly what was updated

## Integration with MoonPress

These fields work seamlessly with MoonPress's `CustomFields` system:

- Each `buy_paperback_*` and `buy_ebook_*` field is stored in `ContentItem.CustomFields`
- Template can use `{{buy_paperback_amazon}}` to display specific links
- Future template helpers can iterate over all `buy_*` fields automatically

## Next Steps

To render these links in your templates, you can either:

1. **Manual approach**: Add `{{buy_paperback_amazon}}` for each retailer in your template
2. **Smart approach**: Create a template helper that automatically generates HTML for all buy links (see MoonPress enhancement plan)

## Notes

- The universal `buy_link` field (books2read) is preserved for backward compatibility
- Retailer names are case-insensitive and special characters are converted to underscores
- Links are alphabetically sorted within each section for consistency
