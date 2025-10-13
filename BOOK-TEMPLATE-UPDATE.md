# Book Template Update - Buy Links Display

## What Was Done

Updated the book template (`themes/aadotcom-v2/templates/book.html`) to **conditionally display all retailer buy links** from the frontmatter.

## Architecture

### Template Structure

```html
<div class="cta">
    <!-- Universal link (books2read) - shows if present -->
    {{#buy_link}}
    <h2><a href="{{buy_link}}" class="buy-button-primary">Buy Now (All Formats)</a></h2>
    {{/buy_link}}
    
    <!-- Paperback section -->
    <h3>Paperback</h3>
    <div class="buy-links paperback-links">
        {{#buy_paperback_amazon}}<a href="{{buy_paperback_amazon}}" ...>Amazon</a>{{/buy_paperback_amazon}}
        <!-- ... more retailers ... -->
    </div>

    <!-- eBook section -->
    <h3>eBook</h3>
    <div class="buy-links ebook-links">
        {{#buy_ebook_kobo}}<a href="{{buy_ebook_kobo}}" ...>Kobo</a>{{/buy_ebook_kobo}}
        <!-- ... more retailers ... -->
    </div>
</div>
```

### How Conditionals Work

MoonPress uses `{{#field}}...{{/field}}` syntax:
- **If field exists and has value**: Shows the content between tags
- **If field is empty or missing**: Removes entire section

This means:
- ✅ Books WITH links → Links display beautifully
- ✅ Books WITHOUT links → Section is hidden (no empty buttons)

### Supported Retailers

**Paperback (7 retailers):**
- AbeBooks
- Amazon
- Barnes & Noble
- Bookshop.org
- LibroWorld
- Readings
- Walmart

**eBook (10 retailers):**
- Apple Books
- Barnes & Noble
- Everand
- Fable
- Google Play
- Kobo
- Palace Marketplace
- Smashwords
- Thalia
- Vivlio

### CSS Styling

Added to `book-styles.css`:

**Features:**
- Responsive flexbox layout
- Hover effects (lift + shadow)
- Mobile-optimized sizing
- Grouped by format (Paperback/eBook)
- Primary CTA button for universal link
- Secondary buttons for individual retailers

**Colors:**
- Primary button: Blue (#007bff)
- Retailer buttons: Light gray with borders
- Hover: Subtle lift with shadow

## Benefits

### ✅ Automatic
- Add links to `book-links.json`
- Run `update-book-links.py`
- Regenerate site → Links appear!

### ✅ Conditional
- No broken links or empty sections
- Each book shows only its available retailers
- Gracefully handles missing data

### ✅ Maintainable
- All retailers in one template
- Add new retailer? Add one line to template
- No hardcoded URLs in template

### ✅ User-Friendly
- Clear format separation (Paperback vs eBook)
- Multiple purchase options
- Universal link at top for convenience

## Usage Example

**Before** (old template):
```html
<a href="{{buy_link}}" class="buy-button">Buy Now</a>
```

**After** (new template):
- Shows universal "Buy Now" button (all formats)
- Shows 7 paperback retailer buttons
- Shows 9 ebook retailer buttons
- All organized by format with clear headings

## Future Enhancements

### Easy Additions

**Add a new retailer:**
1. Add to template: `{{#buy_ebook_newstore}}<a href="{{buy_ebook_newstore}}">NewStore</a>{{/buy_ebook_newstore}}`
2. Add to book-links.json
3. Run update script
4. Done!

**Add format icons:**
```html
<a href="{{buy_paperback_amazon}}">
    📚 Amazon Paperback
</a>
```

**Add retailer logos:**
```html
<a href="{{buy_ebook_kobo}}">
    <img src="/logos/kobo.png" alt="Kobo">
</a>
```

## Testing

Tested with:
- ✅ **The Green Beast**: Has full links (7 paperback + 9 ebook) → All display correctly
- ✅ **Dr. Vortex**: Has only universal link → Only universal button shows
- ✅ **Mobile view**: Buttons resize appropriately
- ✅ **Hover effects**: Smooth transitions and shadows

## Related Files

- `themes/aadotcom-v2/templates/book.html` - Template with conditionals
- `themes/aadotcom-v2/book-styles.css` - Buy button styles
- `content/book-links.json` - Retailer links database
- `update-book-links.py` - Script to update markdown files
- `content/books/*.md` - Book markdown files with frontmatter

## Architecture Principles Followed

- ✅ **Separation of Concerns**: Data (JSON) → Processing (Python) → Storage (Markdown) → Display (Template)
- ✅ **DRY**: One template handles all books
- ✅ **KISS**: Simple conditional syntax, no complex logic
- ✅ **Open/Closed**: Easy to add new retailers without modifying core
