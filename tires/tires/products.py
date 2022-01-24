import json
from pathlib import Path

from scrapy.exceptions import CloseSpider
from woocommerce import API

from tires.tires.utils import HOST_URL, C_KEY, S_KEY


class WooProducts:
    def __init__(self, *args, **kwargs):

        self.wpap = API(
            url=HOST_URL,
            consumer_key=C_KEY,
            consumer_secret=S_KEY,
            query_string_auth=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
            timeout=30
        )

    def product_list(self):
        try:
            with Path('product.json').open(mode='r', encoding='utf-8') as f:
                data = json.loads(f.read())
            if len(data) == int(self.read_index()) + 1:
                data = self.__fetch_product()
                self.__write_json(data)
                self.update_index(0)
        except:
            data = self.__fetch_product()
            if data:
                self.__write_json(data)
            pass
        return data

    def __fetch_product(self):
        p = int(self.__fetch_page())
        products = self.wpap.get(
            'products', params={'per_page': 50, 'page': p})
        if products.status_code == 200:
            p += 1
            self.__write_page(p)

            return products.json()
        else:
            raise CloseSpider(
                f'{products.status_code} Product fetching issue) ')

    def create_product(self, item):
        product = {
            "name": item.get('name'),
            "type": item.get('type'),
            "price": item.get('price'),
            "sku": item.get('ref'),
            "regular_price": item.get('regular_price'),
            "description": item.get('description'),
            "short_description": item.get('short_description'),
            "stock_quantity": item.get('stock'),
            "categories": [
                {'id': int(item['cat'])},
            ],
            "images": [
                {
                    "src": item.get('image_path')
                }
            ]
        }
        self.wpap.post("products", product)

    def update_product(self, item):
        sku = item.get('ref')
        product = self.wpap.get('products/?sku=' + sku).json()
        id = product[0]['id']
        data = {
            "name": item.get('name'),
            "price": item.get('price'),
            "regular_price": item.get('regular_price'),
            "short_description": item.get('short_description'),
            "stock_quantity": item.get('stock'),

        }
        return self.wpap.put('products/{}'.format(id), data)

    @property
    def __is_exist(self):
        return Path('index.json').exists()

    # def get_categories(self, page):
    #     categories = self.wpap.get('products/categories', params={'per_page': 100, 'page': page}).json()
    #     return categories
    def get_or_create_category(self, cat):
        result = self.wpap.get('products/categories/?slug={}'.format(cat.lower())).json()
        if len(result) > 0:
            cat = result[0]
            id = cat['id']
            return id
        else:
            data = {
                "name": cat,
            }
            result = self.wpap.post('products/categories', data).json()
            if result:
                cat = result['id']
                return cat

    def __write_json(self, json_data):
        f = Path('product.json').open(mode='w', encoding='utf-8')
        json.dump(json_data, f, indent=4)
        f.close()

    def read_index(self):
        if self.__is_exist:
            f = Path('index.json').open(mode='r', encoding='utf-8')
            rData = json.loads(f.read())
            f.close()
            s = rData[0].get("index")
            return s
        else:
            return 0

    def __write_page(self, i):
        index = [{"page": i}]
        f = Path('page.json').open(mode='w', encoding='utf-8')
        json.dump(index, f, indent=4)
        f.close()

    def update_index(self, i):
        index = [{"index": i}]
        f = Path('index.json').open(mode='w', encoding='utf-8')
        json.dump(index, f, indent=4)
        f.close()

    def __fetch_page(self):
        if self.__is_page_exist:
            f = Path('page.json').open(mode='r', encoding='utf-8')
            rData = json.loads(f.read())
            f.close()
            s = rData[0].get("page")
            return s
        return 1

    @property
    def __is_page_exist(self):
        return Path('page.json').exists()
