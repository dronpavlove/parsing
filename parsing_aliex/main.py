import json
from time import sleep
import requests
from bs4 import BeautifulSoup


def get_urls_list(url: str, tag: str, tag_class: str, page_count=1):
    """
    Возвращает словарь список словарей о товарах [{name: ___, href: ___}]
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
            urls.append({"name": obj.find("div", class_="product-snippet_ProductSnippet__name__lido9p").text,
                         "href": url_home + obj.find('a').get('href')})
    return urls


def get_product_info(url: str, data: dict):
    """
    Возвращает детальную информацию о товаре
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }
    prod_info = {}
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.text, "lxml")
    prod_info["name"] = data.get("name")
    prod_info["href_aliexpress"] = url
    try:
        prod_info["price"] = soup.find("div", class_="snow-price_SnowPrice__mainS__18x8np").text  # snow-price_SnowPrice__mainS__18x8np
    except:
        prod_info["price"] = '???'
    prod_info["info"] = [i.text for i in soup.find_all("p") if i.text != ''][3:-4:]
    prod_info["photos"] = [i.get('src') for i in soup.find_all('img', class_="gallery_Gallery__image__re6q0q")]
    return prod_info


def main(add_url='category/202001892/men-clothing.html', page_count=1):
    if add_url[-1] == '/':
        file_name = add_url.split('/')[-2]
    else:
        file_name = add_url.split('/')[-1]
    product_dict = get_urls_list(url=f"https://aliexpress.ru/{add_url}/",
                                 tag="div", tag_class="product-snippet_ProductSnippet__description__lido9p",
                                 page_count=page_count)
    product_list = []
    for i in product_dict:
        print(i)
        sleep(10)
        product_list.append(get_product_info(url=i.get("href"), data=i))
    with open(f"data/{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(product_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    plus_url = input('Введите продолжение строки https://aliexpress.ru/')  # category/202001892/men-clothing.html
    pg_count = int(input('Введите количество страниц для обработки: '))
    main(add_url=plus_url, page_count=pg_count)
