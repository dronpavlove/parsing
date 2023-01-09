import json
import requests
from bs4 import BeautifulSoup


def get_urls_list(url: str, tag: str, tag_class: str, page_count=1):
    """
    Возвращает ссылки на детальные страницы товаров
    """
    urls = []
    url_list = url.split('/')
    url_home = url_list[0] + '//' + url_list[2]
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }
    for num in range(1, page_count + 1):
        url = url + f"?page={num}"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.text, "lxml")
        result_tuple = soup.find_all(tag, class_=tag_class)
        for obj in result_tuple:
            urls.append(url_home + obj.get('href'))
    return urls


def get_product_info(url: str):
    """
    Возвращает детальную информацию о товаре
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }
    prod_info = {}
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.text, "lxml")
    prod_info["href_lamoda"] = url
    try:
        prod_info["name"] = soup.find("div", class_="x-premium-product-title__model-name").text
    except:
        prod_info["name"] = '---'
    try:
        prod_info["price"] = [i.text for i in soup.find_all("span", class_="x-premium-product-prices__price")]
    except:
        prod_info["price"] = []
    result_tuple = soup.find_all("p")
    prod_info["info"] = []
    prod_info["photos"] = []

    for i in result_tuple:
        try:
            prod_info["info"].append({
                i.find('span', class_="x-premium-product-description-attribute__name").text: i.find('span', class_="x-premium-product-description-attribute__value").text
            })
        except:
            pass

    for img in soup.find_all('img'):
        prod_info["photos"].append('https:' + img.get('src'))
    return prod_info


def main(add_url='c/23/shoes-botinki', page_count=1):
    if add_url[-1] == '/':
        file_name = add_url.split('/')[-2]
    else:
        file_name = add_url.split('/')[-1]
    a = get_urls_list(url=f"https://www.lamoda.ru/{add_url}/",
                      tag="a", tag_class="x-product-card__link x-product-card__hit-area",
                      page_count=page_count)
    product_list = []
    for i in a:
        product_list.append(get_product_info(url=i))
    with open(f"data/{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(product_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    plus_url = input('Введите продолжение строки https://www.lamoda.ru/')
    pg_count = int(input('Введите количество страниц для обработки: '))
    main(add_url=plus_url, page_count=pg_count)
