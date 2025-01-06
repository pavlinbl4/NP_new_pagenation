from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger
from requests import Session

from gui_tools.select_month import select_month
from image_downloader import downloader

logger.disable('__main__')
# pip install lxml

icloud_folder = Path().home() / 'Library/Mobile Documents/com~apple~CloudDocs/'


def date_convert(month_number):
    months = {
        1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
        7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
    }
    return months.get(month_number, 'Invalid month')


def get_previous_month(month_number):
    if month_number == 1:
        return 12
    return month_number - 1


def cook_soup(count, base_url):
    headers = {
        'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/127.0.0.0 Safari/537.36'
    }
    s = Session()
    s.headers.update(headers)
    work_url = f'{base_url}/?article={count}&pageId=1&hash=cbf05cb35393866fb263316a822d653e4971ece5'

    try:
        response = s.get(work_url)
        response.raise_for_status()  # Проверяет статус ответа
    except Exception as e:
        logger.error(f"Ошибка при запросе {work_url}: {e}")
        return None

    return BeautifulSoup(response.text, 'lxml')


def main(month_number):
    base_url = 'https://newprospect.ru'
    count = 1

    while count < 15:
        soup = cook_soup(count, base_url)
        extract_article_data(base_url, soup, month_number)
        count += 1


def extract_article_data(base_url, soup, month_number):
    month_name = date_convert(month_number)
    previous_month_name = date_convert(get_previous_month(month_number))

    # find all articles on page
    articles = soup.find_all('div', class_="tplarticle")

    for article in articles:

        # get date of article
        article_date_tag = article.find('div', class_="tplarticle-date")
        if not article_date_tag:
            logger.warning("Дата статьи не найдена")
            continue

        article_date = article_date_tag.text.strip()
        if len(article_date.split(' ')) < 3:
            logger.warning(f"Некорректный формат даты: {article_date}")
            continue

        article_year = article_date.split(' ')[2]

        # if found name of last month stop working
        if previous_month_name in article_date:
            break

        article_name = article.find('div', class_="tplarticle-title").text.strip()
        image_tag = article.find('img', class_='tplarticle-img lazyload')

        if not image_tag or not image_tag.get('data-src'):
            logger.warning("Изображение не найдено")
            continue

        article_image_link = f"{base_url}{image_tag.get('data-src')}"
        image_name = f'{article_date}__{article_name}'

        if month_name in article_date:
            print(article_date, article_name, article_image_link)

            folder_path = icloud_folder / f"Documents/NewProspect/{article_year}_{month_number}"
            folder_path.mkdir(parents=True, exist_ok=True)

            downloader(article_image_link, image_name, folder_path=folder_path)


if __name__ == '__main__':
    _month_number = select_month()
    main(_month_number)

    # _soup = cook_soup(1, 'https://newprospect.ru')
    #
    # print(extract_article_data('https://newprospect.ru',
    #                            _soup, 1))
