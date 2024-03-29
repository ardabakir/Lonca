from dataclasses import dataclass

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
    status:str
    isDiscounted: bool
    price_unit: str = "USD"
    
    #constructor
    def __init__(self, product):
        for key, val in product.items():
           setattr(self, key, val)
        if self.discounted_price < self.price:
            self.isDiscounted = True
        else:
            self.isDiscounted = False
        if self.quantity > 0:
            self.status = "Active"
        else:
            self.status = "Inactive"