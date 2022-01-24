# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import TakeFirst, MapCompose
from scrapy.item import Item, Field

from .utils import remove_tag, price_increase


def split_ref(ref):
    reference = ref.split(':')[1]
    sku_string = f'neu{reference.strip()}'
    return sku_string


class TiresItem(Item):
    name = Field(
        input_processor=MapCompose(remove_tag),
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(remove_tag, price_increase),
        output_processor=TakeFirst()

    )
    regular_price = Field(
        input_processor=MapCompose(remove_tag, price_increase),
        output_processor=TakeFirst()

    )
    stock = Field(
        input_processor=MapCompose(remove_tag),

        output_processor=TakeFirst()
    )
    ref = Field(
        input_processor=MapCompose(split_ref),
        output_processor=TakeFirst()
    )
    image_path = Field(
        output_processor=TakeFirst()
    )
    description = Field(
        output_processor=TakeFirst()
    )
    short_description = Field(
        output_processor=TakeFirst()
    )

    type = Field(
        output_processor=TakeFirst()
    )
    cat = Field(
        output_processor=TakeFirst()
    )
