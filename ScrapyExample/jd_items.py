from scrapy import Item,Field

class JdItem(Item):
    ID = Field()   
    name = Field() 
    link = Field()
    brand = Field()
    weight = Field()
    net_weight = Field()
    place = Field()
    origin_place = Field()
    category = Field()
    dome_import = Field()
    price = Field()
    variety = Field()
    shop_name = Field()
    packing = Field()
    cook = Field()

