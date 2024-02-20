import json
import xml.etree.ElementTree as ET
import xmltodict

from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://root:example@localhost/lonca?authSource=admin&retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['local']
  
# This is added so that many files can reuse the function get_database()

  
# Get the database
dbname = get_database()



# Path to the XML file
xml_file_path = "./lonca-sample.xml"

#Read xml file
with open(xml_file_path, 'r', encoding="utf8") as file:
    data = file.read()

    prod_dict = xmltodict.parse(data)
    print(json.dumps(prod_dict, indent=2))

    # Insert the data into the database
    dbname['products'].insert_many(prod_dict["Products"]["Product"])


# # Parse the XML file
# tree = ET.parse(xml_file_path)
# root = tree.getroot()

# # Iterate over the elements in the XML file
# for element in root:
#     # Process each element as needed
#     print(element.attrib["ProductId"])
#     print(element.attrib["Name"])
#     productDetails = element.find('ProductDetails')
#     for productDetail in productDetails:
#         print(productDetail.attrib["Name"],productDetail.attrib["Value"])

#     print("-------------------------------------------------")    