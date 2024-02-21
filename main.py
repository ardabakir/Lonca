import datetime
import json
import xml.etree.ElementTree as ET
import xmltodict
from bs4 import BeautifulSoup
from Database import Database
from Product import Product
from pymongo import MongoClient
  
# def arrange_product_data(product):
#     product_data = {}
#     product_data["_id"] = product["@ProductId"]
#     product_data["name"] = product["@Name"]
#     for productDetail in product["ProductDetails"]["ProductDetail"]:
#         product_data[productDetail["@Name"].lower()] = str(productDetail["@Value"])
#     product_data["images"] = []
#     for image in product["Images"]["Image"]:
#         product_data["images"].append(image["@Path"])
#     return product_data

# def parse_description(description):
#     #parse html content in the description using beautifulsoup
#     soup = BeautifulSoup(description, 'html.parser')
#     list_items = soup.find_all('li')
#     desc_dict = {}
#     for item in list_items:
#         bold = item.find('strong')
#         if bold != None:
#             colon_index = bold.text.find(':')
#             if colon_index != -1:
#                 desc_dict[bold.text[:colon_index].strip()] = item.text[colon_index+1:].strip()
#     return desc_dict

#setup db connection using Database class
db = Database()

# Path to the XML file
xml_file_path = "./lonca-sample.xml"

#Read xml file
# with open(xml_file_path, 'r', encoding="utf8") as file:
#     data = file.read()

#     prod_dict = xmltodict.parse(data, process_namespaces=True)
#     print(json.dumps(prod_dict, indent=2))

#     # Insert the data into the database
#     # check if the item exists before inserting
#     # if it exists, update the item
#     for product in prod_dict["Products"]["Product"]:
#         db_item = dbname['products'].find_one({"_id": product["@ProductId"]})
#         if db_item == None:
#             dbname['products'].insert_one(arrange_product_data(product))
#         else:
#             dbname['products'].update_one({"_id": product["@ProductId"]}, {"$set": arrange_product_data(product)})
#             print("Updated: ", product["@ProductId"])

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Iterate over the elements in the XML file
for element in root:
    # Process each element as needed
    product_obj = Product(element)
    # upsert product_obj to the database using Database class
    db.upsert_data(product_obj)