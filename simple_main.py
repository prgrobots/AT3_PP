import json

class ProductManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.products = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as dbase:
                return json.load(dbase)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.data_file, 'w') as dbase:
            json.dump(self.products, dbase, indent=4)

    def get_products(self):
        return self.products

    def add_or_update_product(self, product_name, price, emoji):
        for product in self.products:
            if product['name'] == product_name:
                product['price'] = price
                product['emoji'] = emoji
                break
        else:
            self.products.append({'name': product_name, 'price': price, 'emoji': emoji})
        self.save_data()

class View:
    def display_main_menu(self):
        print("\nMain Menu:")
        print("1. Buy Products")
        print("2. Admin Login")
        print("3. Quit")

    def display_admin_login(self):
        print("\nAdmin Login:")
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        return username, password

    def display_admin_menu(self):
        print("\nAdmin Menu:")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Main Menu")
        print("4. Quit")

    def display_add_product(self):
        print("\nAdd Product:")
        product_name = input("Enter product name: ")
        price = input("Enter price: ")
        emoji = input("Enter emoji: ")
        return product_name, price, emoji

    def display_update_product(self):
        print("\nUpdate Product:")
        product_name = input("Enter product name: ")
        price = input("Enter price: ")
        emoji = input("Enter emoji: ")
        return product_name, price, emoji

    def display_products(self, products):
        if not products:
            print("No products available.")
        else:
            print("\nProducts:")
            for product in products:
                print(f"{product['name']} - ${product['price']} - {product['emoji']}")

    def display_order_details(self, order_details, total_price):
        print("\nOrder Details:")
        for item in order_details:
            print(f"{item['name']} x {item['quantity']} @ ${item['price']} = ${item['total']}")
        print(f"Total: ${total_price}")

    def confirm_order(self):
        confirm = input("Confirm order? (y/n) ").lower()
        return confirm == 'y'

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_main_menu()
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
        products = self.model.get_products()
        self.view.display_products(products)

        if products:
            product_name = input("Enter the product name to order: ")
            quantity = int(input("Enter the quantity: "))
            total_price = 0
            order_details = []

            for product in products:
                if product['name'] == product_name:
                    price = float(product['price'])
                    item_total = price * quantity
                    total_price += item_total
                    order_details.append({
                        'name': product_name,
                        'quantity': quantity,
                        'price': price,
                        'total': item_total
                    })
                    break
            else:
                print(f"Product '{product_name}' not found.")
                return

            self.view.display_order_details(order_details, total_price)
            if self.view.confirm_order():
                print("Order confirmed.")
            else:
                print("Order canceled.")

    def admin_login(self):
        username, password = self.view.display_admin_login()
        # TODO: Validate admin credentials
        self.admin_menu()

    def admin_menu(self):
        while True:
            self.view.display_admin_menu()
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                break
            elif choice == '4':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

    def add_product(self):
        product_name, price, emoji = self.view.display_add_product()
        self.model.add_or_update_product(product_name, price, emoji)

    def update_product(self):
        product_name, price, emoji = self.view.display_update_product()
        self.model.add_or_update_product(product_name, price, emoji)

if __name__ == "__main__":
    model = ProductManager('database.json')
    view = View()
    controller = Controller(model, view)
    controller.run()