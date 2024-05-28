import json

class ProductManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.products = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.products, file, indent=4)

    def get_products(self):
        return self.products

    def add_product(self, product_name, price, emoji):
        for product in self.products:
            if product['name'] == product_name:
                product.update({'price': price, 'emoji': emoji})
                print(f"Product '{product_name}' updated.")
                self.save_data()
                return
        self.products.append({'name': product_name, 'price': price, 'emoji': emoji})
        print(f"Product '{product_name}' added.")
        self.save_data()

    def place_order(self, product_name, quantity):
        for product in self.products:
            if product['name'] == product_name:
                price = float(product['price'])
                total_price = price * quantity
                print(f"Order Details:\n{product_name} x {quantity} @ ${price} = ${total_price}\nTotal: ${total_price}")
                confirm = input("Confirm order? (y/n) ").lower()
                print("Order confirmed." if confirm == 'y' else "Order canceled.")
                return
        print(f"Product '{product_name}' not found.")

class Application:
    def __init__(self):
        self.product_manager = ProductManager('data.json')
        self.run()

    def run(self):
        while True:
            print("\nMain Menu:\n1. Buy Products\n2. Admin Login\n3. Quit")
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                self.show_products()
            elif choice == '2':
                self.admin_login()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_products(self):
        products = self.product_manager.get_products()
        if not products:
            print("No products available.")
        else:
            for product in products:
                print(f"{product['name']} - ${product['price']} - {product['emoji']}")
            product_name = input("Enter the product name to order: ")
            quantity = int(input("Enter the quantity: "))
            self.product_manager.place_order(product_name, quantity)

    def admin_login(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        # TODO: Validate admin credentials
        self.admin_menu()

    def admin_menu(self):
        while True:
            print("\nAdmin Menu:\n1. Add/Update Product\n2. Main Menu\n3. Quit")
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                self.add_product()
            elif choice == '2':
                break
            elif choice == '3':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

    def add_product(self):
        product_name = input("Enter product name: ")
        price = input("Enter price: ")
        emoji = input("Enter emoji: ")
        self.product_manager.add_product(product_name, price, emoji)

if __name__ == "__main__":
    app = Application()
