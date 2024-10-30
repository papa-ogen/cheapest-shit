from app.models.product import Product
from app.services.scrape import scrape_xxl

class ProductService:
    @staticmethod
    def get_all_products() -> list[Product]:
        products = scrape_xxl()
        return products

    @staticmethod
    def create_product(product_data) -> Product:
        # Logic to save the product to the database
        return Product(name=product_data.name, price=product_data.price, description=product_data.description)