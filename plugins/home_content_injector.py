from pelican import signals
import os
import re

def update_homepage_with_books(generator):
    content_path = generator.settings['PATH']
    home_md_path = os.path.join(content_path, 'pages', 'home.md')

    # Find the latest 3 "Books" articles
    books = [article for article in generator.articles if article.category.name == "Books"]
    books.sort(key=lambda a: a.date, reverse=True)
    latest_books = books[:3]

    # Format the entries
    new_content = "\n".join([f"- [{a.title}]({a.url}) ({a.date.strftime('%Y-%m-%d')})" for a in latest_books])

    # Replace section in home.md
    with open(home_md_path, 'r', encoding='utf-8') as f:
        contents = f.read()

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
