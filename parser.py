import grequests

from bs4 import BeautifulSoup


def parse_data(html_code):
    """Parsing HTML of category and return list of goods."""

    soup = BeautifulSoup(html_code, 'lxml')
    list_products_html_code = soup.find_all('div', class_='product')
    data_list = []
    for product in list_products_html_code:
        product_name = product.find_all('a')[1].text
        product_price = product.find('div', class_='price').text.replace(' ', '')[1:]  # del white spaces and '/n'
        data_list.append({'name': product_name, 'price': product_price})
    return data_list


def get_goods_data():
    """Request categories url and return list of goods."""

    list_catalog_url = ['https://megamarket.ua/ua/catalogue/category/{0}?'
                        'show=48000'.format(x) for x in range(1010, 1120, 10)]
    requests_gen = (grequests.get(url) for url in list_catalog_url)
    response_list = grequests.map(requests_gen)
    data = []
    for response in response_list:
        catalog_data = parse_data(response.text)
        data.extend(catalog_data)
    return data


def main():
    """Print goods list."""

    print(get_goods_data())


if __name__ == '__main__':
    main()
