from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
from .products import WooProducts


class TiresPipeline():
    current_category = ''
    previous_category = ''
    cat_id = 0

    def open_spider(self, spider):
        self.wpap = WooProducts()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.current_category = adapter.get('cat')
        if self.previous_category == '' or self.previous_category != self.current_category:
            self.cat_id = self.wpap.get_or_create_category(self.current_category)
            self.previous_category = self.current_category

        adapter['cat'] = self.cat_id
        if spider.name == 'create':
            self.wpap.create_product(item)
        elif spider.name == 'update':
            self.wpap.update_product(item)
        return item
