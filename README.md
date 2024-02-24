# Product Entry Case Study

In this project I wanted to use Etl class to handle the extract, transform and load operations to divide up the work.

I also used a Database class to instantiate the database connection and a Product dataclass to be saved into the database.

Extract and load parts of the Etl are relatively simple compared to the transform part. In the extract method I am only reading the data from the given file. In the load method I am writing the data into the database.

## Transfroming the Data

In the transform method I first converted the data to a dictionary using an external library called xmltodict to access each tag more easily. 

arrange_product_data method, called in transform method, iterates over each product found in the newly created dictionary and creates a Product object for each of them. ıt gets the required fields from the given data and modifies the keys or values when necessary to match the output format. 
For the productDetails part I iterate over each product detail item and change the key or value when necessary. 

For the description tag I decided to use another external library called BeautifulSoup to parse the html text stored in the description. I noticed that there is a pattern where each of the keys are written inside a "strong" tag. However, not all strong tags are keys. I decided to use the colons written after the potential keys to split the text, and changed the key names to match the example output. For the sample size value I assumed that it would allways be written inside strong tags and wouldn't contain a colon, since it was the case for all of the products given in the xml file.

## Product 

I created the Product dataclass to bette organize the structure of the data to be put into the database. In this project I didn't used any functionality of the Product dataclass except from calculating some of the values from the given data.

## Writing to Database

I created an upsert_many method inside the Database class, which calls the update_one method for each item. In the update_one method I set upsert parameter to True to avoid any multiple inserts for the same data and I add createdAt and updatedAt fields for the data in the update parameter. 


#### Assumptions about the Data

The color field would be separated by commas if there were multiple colors were listed in one product. 
The isDiscounted value is false when the discounted_price and price values are the same, and true if otherwise.
The status value is "Active" if quantity is greater than zero, and "Inactive" otherwise.
The price_unit value is "USD" by default and it would be given inside a ProductDetail tag. 