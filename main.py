import os
from bs4 import BeautifulSoup, element

from web import get_page, get_remote_list
from article import Article

dir = "tmp"

if not os.path.exists(dir):
    os.makedirs(dir)

existing_list = get_remote_list()


def extract_articles(soup):
    article_list = list()
    article_list.append(
        Article(soup.find('div', {'class': 'article-feature'}).article))
    articles = soup.find('div', {'class': 'article-list'}).children

    for child in articles:
        if (type(child) == element.NavigableString):
            continue
        if (child.name != 'article'):
            continue
        if (child.div.div.div.h4.a.contents[0].find('Survey: ') >= 0):
            continue
        article_list.append(Article(child))

    print("found {} articles.".format(len(article_list)))

    article_list.reverse()

    return article_list


def sync_file(article):
    print()
    if article.get_name_without_index() in existing_list:
        print("{} exists, skipping.".format(article.get_original_name()))
        return

    article.load_pdf(dir)


src = BeautifulSoup(get_page(), features='html.parser')
articles = extract_articles(src)

for i, article in enumerate(articles):
    article.set_index(i + 1)
    sync_file(article)

# clearing temp folder
print("clearing cache...")
tmp_files = os.listdir(dir)

for file in tmp_files:
    os.remove("{}/{}".format(dir, file))
print("done!")
