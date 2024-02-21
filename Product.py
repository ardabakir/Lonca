from dataclasses import dataclass
from bs4 import BeautifulSoup

@dataclass
class Product:
    stock_code: str
    name: str
    images: list
    price: float
    discounted_price: float
    quantity: int
    color: list
    series: str
    season: str
    product_type: str
    fabric: str
    model_measurements: str
    product_measurements: str
    sample_size: str
    
    #constructor
    def __init__(self, product):
        self.__set_fields(product)

    def __set_fields(self,product):
        self.stock_code = product.attrib["ProductId"]
        self.name = product.attrib["Name"]
        self.images = []
        for image in product.find('Images'):
            self.images.append(image.attrib["Path"])
        for productDetail in product.find('ProductDetails'):
            if productDetail.attrib["Name"].lower() == "price":
                self.price = productDetail.attrib["Value"]
            elif productDetail.attrib["Name"].lower() == "discountedprice":
                self.discounted_price = productDetail.attrib["Value"]
            elif productDetail.attrib["Name"].lower() == "quantity":
                self.quantity = productDetail.attrib["Value"]
            elif productDetail.attrib["Name"].lower() == "color":
                self.color = []
                for color in productDetail.attrib["Value"].split(','):
                    self.color.append(color.strip())
            elif productDetail.attrib["Name"].lower() == "series":
                self.series = productDetail.attrib["Value"]
            elif productDetail.attrib["Name"].lower() == "season":
                self.season = productDetail.attrib["Value"]
            elif productDetail.attrib["Name"].lower() == "producttype":
                self.product_type = productDetail.attrib["Value"]
        soup = BeautifulSoup(product.find("Description").text, 'html.parser')
        list_items = soup.find_all('li')

        for item in list_items:
            bold = item.find('strong')
            if bold != None:
                colon_index = bold.text.find(':')
                if colon_index != -1:
                    key = bold.text[:colon_index].strip().lower()
                    if key == "kumaş bilgisi":
                        self.fabric = item.text[colon_index+1:].strip()
                    elif key == "model ölçüleri":
                        self.model_measurements = item.text[colon_index+1:].strip()
                    elif key == "ürün ölçüleri":
                        self.product_measurements = item.text[colon_index+1:].strip()
                else:
                    self.sample_size = bold.text.strip()
