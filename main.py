from bs4 import BeautifulSoup
from requests import Session

from image_downloader import downloader


# pip install lxml

def cook_soup(count, base_url):
    headers = {'user-agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/127.0.0.0 Safari/537.36'}
    s = Session()
    s.headers.update(headers)
    work_url = f'{base_url}/?article={count}&pageId=1&hash=cbf05cb35393866fb263316a822d653e4971ece5'
    response = s.get(work_url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def main():
    base_url = 'https://newprospect.ru'
    count = 1
    while count < 12:
        soup = cook_soup(count, base_url)
        extract_article_data(base_url, soup)
        count += 1


def extract_article_data(base_url, soup):
    # find all articles on page
    articles = soup.find_all('div', class_="tplarticle")

    for article in articles:

        # get date of article
        article_date = article.find('div', class_="tplarticle-date").text

        # if found name of last month stop working
        if 'Июня' in article_date:
            break

        article_name = article.find('div', class_="tplarticle-title").text
        article_image_link = f"{base_url}{article.find('img', class_='tplarticle-img lazyload').get('data-src')}"

        image_name = f'{article_date}__{article_name}'

        if 'Июля' in article_date:
            print(article_date, article_name, article_image_link)
            # download images
            downloader(article_image_link, image_name, folder_path='/Volumes/big4photo/Documents/NewProspect/2024_7')


if __name__ == '__main__':
    main()
