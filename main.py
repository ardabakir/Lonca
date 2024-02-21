import datetime
import json
import xml.etree.ElementTree as ET
import xmltodict
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://root:example@localhost/lonca?authSource=admin&retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['local']
  
def arrange_product_data(product):
    product_data = {}
    product_data["_id"] = product["@ProductId"]
    product_data["name"] = product["@Name"]
    for productDetail in product["ProductDetails"]["ProductDetail"]:
        product_data[productDetail["@Name"].lower()] = str(productDetail["@Value"])
    product_data["images"] = []
    for image in product["Images"]["Image"]:
        product_data["images"].append(image["@Path"])
    return product_data

def parse_description(description):
    #parse html content in the description using beautifulsoup
    soup = BeautifulSoup(description, 'html.parser')
    list_items = soup.find_all('li')
    desc_dict = {}
    for item in list_items:
        bold = item.find('strong')
        if bold != None:
            colon_index = bold.text.find(':')
            if colon_index != -1:
                desc_dict[bold.text[:colon_index].strip()] = item.text[colon_index+1:].strip()
    return desc_dict

# Get the database
dbname = get_database()



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
    product_dict = {}
    product_dict["_id"] = element.attrib["ProductId"]
    product_dict["name"] = element.attrib["Name"]
    productDetails = element.find('ProductDetails')
    for productDetail in productDetails:
        product_dict[productDetail.attrib["Name"].lower()] = productDetail.attrib["Value"]
        print(productDetail.attrib["Name"],productDetail.attrib["Value"])
    images = element.find('Images')
    image_list = []
    for image in images:
        image_list.append(image.attrib["Path"])
    product_dict["images"] = image_list
    desc = element.find('Description')
    for item in parse_description(desc.text):
        product_dict[item] = parse_description(desc.text)[item]
    now = datetime.datetime.now()
    dbname['products'].update_one(product_dict,update={'$setOnInsert':{'createdAt':now,},'$set':{'updatedAt':now,},}, upsert=True)
    