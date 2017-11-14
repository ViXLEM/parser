import grequests

from app import celery
from config import SECRET_URL
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def parse_data(html_code):
    """Parse HTML of category and return list of goods."""

    soup = BeautifulSoup(html_code, 'lxml')
    list_products_html_code = soup.find_all('div', class_='product')
    data_list = []
    for product in list_products_html_code:
        product_name = product.find_all('a')[1].text
        product_price = product.find('div', class_='price').text.replace(' ', '')[1:]  # del white spaces and '/n'
        data_list.append({'name': product_name, 'price': product_price})
    logger.info('End parse HTML code...')
    return data_list


@celery.task
def get_goods_data():
    """Request categories url and return list of goods."""

    logger.info('Starting fetch data...')
    list_catalog_url = ['https://megamarket.ua/ua/catalogue/category/{0}?'
                        'show=48000'.format(x) for x in range(1010, 1120, 10)]
    requests_gen = (grequests.get(url) for url in list_catalog_url)
    response_list = grequests.map(requests_gen)
    data = []
    logger.info('Starting parse data...')
    for response in response_list:
        catalog_data = parse_data(response.text)
        data.extend(catalog_data)
    grequests.post(SECRET_URL, data=data)
