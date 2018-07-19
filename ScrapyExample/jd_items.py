from scrapy import Item,Field

class JdItem(Item):
    ID = Field()   
    name = Field() 
    price = Field()
    link = Field()
    shop_name = Field()
    brand = Field()
    weight = Field()
    net_weight = Field()
    place = Field()
    origin_place = Field()
    category = Field()
    dome_import = Field()
