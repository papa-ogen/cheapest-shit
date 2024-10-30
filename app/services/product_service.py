from app.models.product import Product

class ProductService:
    @staticmethod
    def get_all_products() -> list[Product]:
        # Dummy data or database query
        return [Product(name="Sample Product", price=19.99)]

    @staticmethod
    def create_product(product_data) -> Product:
        # Logic to save the product to the database
        return Product(name=product_data.name, price=product_data.price, description=product_data.description)