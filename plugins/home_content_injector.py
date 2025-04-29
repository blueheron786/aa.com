from pelican import signals
import os
import re

NUM_BOOKS = 3

def update_homepage_with_books(generator):
    content_path = generator.settings['PATH']
    home_md_path = os.path.join(content_path, 'pages', 'home.md')

    # Find the latest 3 "Books" articles
    books = [article for article in generator.articles if article.category.name == "Books"]
    books.sort(key=lambda a: a.date, reverse=True)
    latest_books = books[:NUM_BOOKS]

    # Format the entries
    new_content = "\n".join([f"- [{a.title}]({a.url}) (published in {a.date.strftime('%B %Y')})" for a in latest_books])

    # Replace section in home.md
    with open(home_md_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    # Preserve start/end tags so we know what to replace on subsequent searches/replacements.
    updated = re.sub(
        r'<!-- start -->.*?<!-- end -->',
        f'<!-- start -->\n{new_content}\n<!-- end -->',
        contents,
        flags=re.DOTALL
    )

    with open(home_md_path, 'w', encoding='utf-8') as f:
        f.write(updated)

def register():
    signals.article_generator_finalized.connect(update_homepage_with_books)
