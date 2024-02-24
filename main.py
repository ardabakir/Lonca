from Etl import Etl

xml_file_path = "./lonca-sample.xml"

etl = Etl(xml_file_path)
data = etl.extract()
products = etl.transform(data)
etl.load(products)
