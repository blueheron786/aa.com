from pelican import signals
import os
import re

NUM_BOOKS = 3
NUM_BLOG_POSTS = 5

def update_homepage_with_books(generator):
    content_path = generator.settings['PATH']
    home_md_path = os.path.join(content_path, 'pages', 'home.md')

    # Find the latest 3 "Books" articles
    books = [article for article in generator.articles if article.category.name == "Books"]
    books.sort(key=lambda a: a.date, reverse=True)
    latest_books = books[:NUM_BOOKS]

    siteurl = generator.settings.get('SITEURL', '')
    # Format the entries. Similar to books.html's display.
    new_content = "\n".join([f"""
<div class="book-grid">
    <div class="book-image">
        <a href="{siteurl}/{a.url}">
            <img src="{siteurl}{a.metadata.get('cover', '')}" alt="{a.title} cover" />
        </a>
    </div>
    <div class="book-info">
        <h2 class="book-title"><a href="{siteurl}/{a.url}">{a.title}</a></h2>
        <p class="book-summary">{a.summary}</p>
        <p><a class="read-more" href="{siteurl}/{a.url}">Read more →</a></p>
    </div>
</div>
        """ for a in latest_books])
    
    # Replace section in home.md
    with open(home_md_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    # Preserve start/end tags so we know what to replace on subsequent searches/replacements.
    updated = re.sub(
        r'<!-- start books -->.*?<!-- end books -->',
        f'<!-- start books -->\n{new_content}\n<!-- end books -->',
        contents,
        flags=re.DOTALL
    )

    with open(home_md_path, 'w', encoding='utf-8') as f:
        f.write(updated)

def update_homepage_with_blog_posts(generator):
    content_path = generator.settings['PATH']
    home_md_path = os.path.join(content_path, 'pages', 'home.md')

    # Find the latest 3 "Books" articles
    posts = [article for article in generator.articles if article.category.name == "blog"]
    posts.sort(key=lambda a: a.date, reverse=True)
    latest_posts = posts[:NUM_BLOG_POSTS]

    # Format the entries
    new_content = "\n".join([f"- [{a.title}]({a.url}) - {a.date.strftime('%B %-d, %Y')}" for a in latest_posts])

    # Replace section in home.md
    with open(home_md_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    # Preserve start/end tags so we know what to replace on subsequent searches/replacements.
    updated = re.sub(
        r'<!-- start blog posts -->.*?<!-- end blog posts -->',
        f'<!-- start blog posts -->\n{new_content}\n<!-- end blog posts -->',
        contents,
        flags=re.DOTALL
    )

    with open(home_md_path, 'w', encoding='utf-8') as f:
        f.write(updated)

def register():
    signals.article_generator_finalized.connect(update_homepage_with_books)
    signals.article_generator_finalized.connect(update_homepage_with_blog_posts)
