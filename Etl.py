from Database import Database
from Product import Product
from bs4 import BeautifulSoup
import xmltodict


class Etl:

    def __init__(self, file_path):
        self.file_path = file_path

    # Extract data from the file
    def extract(self):
        with open(self.file_path, 'r', encoding="utf8") as file:
            data = file.read()
        return data

    # Transform the data into a format that can be loaded into the database
    def transform(self, data):

        prod_dict = xmltodict.parse(data, process_namespaces=True)

        products = self.__arrange_product_data(prod_dict["Products"]["Product"])

        return products

    # Load the data into the database
    def load(self, data):
        db = Database()
        db.upsert_many(map(lambda x: x.__dict__, data))

    # Arrange the product data into a list of Product objects
    def __arrange_product_data(self, products):
        products_data = []
        for product in products:
            product_data = {}
            product_data["stock_code"] = product["@ProductId"]
            product_data["name"] = product["@Name"]
            for productDetail in product["ProductDetails"]["ProductDetail"]:
                key, val = self.__process_product_detail(productDetail)
                product_data[key] = val
            product_data["images"] = []
            for image in product["Images"]["Image"]:
                product_data["images"].append(image["@Path"])
            
            description = product["Description"]
            for item in self.__parse_description(description):
                product_data[item] = self.__parse_description(description)[item]
            
            products_data.append(Product(product_data))
        return products_data
    

    def __parse_description(self, description):
        #parse html content in the description using beautifulsoup
        soup = BeautifulSoup(description, 'html.parser')
        list_items = soup.find_all('li')
        desc_dict = {}
        #find strong tags in the list items 
        #strong tags are used to identify the description items
        for item in list_items:
            bold = item.find('strong')
            if bold == None:
                continue
            #find the index of the colon in the bold text
            #if the bold text contains a colon, it is a description item
            #if it doesn't contain a colon, it is the sample size
            colon_index = bold.text.find(':')
            if colon_index == -1:
                desc_dict["sample_size"] = bold.text.strip()
                continue
            desc_dict = self.__process_description(item, bold, colon_index, desc_dict)
        return desc_dict
    
    # process the description items to better fit the product data and translate the description keys
    def __process_description(self, item, bold, ind, dict):
        if bold.text[:ind].strip().lower() == "kumaş bilgisi":
                dict["fabric"] = item.text[ind+1:].strip()
        elif bold.text[:ind].strip().lower() == "model ölçüleri":
            dict["model_measurements"] = item.text[ind+1:].strip()
        elif bold.text[:ind].strip().lower() == "ürün ölçüleri":
            dict["product_measurements"] = item.text[ind+1:].strip()

        return dict

    # process the product details and change the key names to better fit the product data
    def __process_product_detail(self, productDetail):
        key = productDetail["@Name"].lower()
        if key == "price":
            key = productDetail["@Name"].lower()
            val = float(productDetail["@Value"].replace(',','.'))
        elif key == "discountedprice":
            key = "discounted_price"
            val = float(productDetail["@Value"].replace(',','.'))
        elif key == "color":
            val = productDetail["@Value"].split(',')
        elif key == "producttype":
            key = "product_type"
            val = productDetail["@Value"]
        elif key == "priceunit":
            key = "price_unit"
            val = productDetail["@Value"]
        else:
            val = productDetail["@Value"]
        return key, val
    