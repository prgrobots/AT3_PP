import tkinter as tk
from tkinter import messagebox
import json

class Application:
    def __init__(self, master, data_file):
        self.master = master
        self.master.title("Growers Produce Sales")
        self.data_manager = DataManager(data_file)
        self.current_frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.master, self)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

    def run(self):
        self.master.mainloop()

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.products = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

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
        self.save_data(self.products)

class BaseFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

class MainMenu(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        tk.Label(self, text="Welcome to Growers Produce Sales").pack()
        tk.Button(self, text="Buy Products", command=lambda: controller.switch_frame(ProductSelection)).pack()
        tk.Button(self, text="Admin Login", command=lambda: controller.switch_frame(AdminLogin)).pack()
        tk.Button(self, text="Quit", command=self.quit).pack()

    def quit(self):
        self.controller.master.quit()

class AdminLogin(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        tk.Label(self, text="Admin Login").pack()
        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        tk.Button(self, text="Login", command=self.validate_login).pack()
        tk.Button(self, text="Main Menu", command=lambda: controller.switch_frame(MainMenu)).pack()

    def validate_login(self):
        # TODO: Validate admin credentials
        self.controller.switch_frame(AdminMenu)

class AdminMenu(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        tk.Label(self, text="Admin Menu").pack()
        tk.Button(self, text="Add Product", command=lambda: controller.switch_frame(AddProduct)).pack()
        tk.Button(self, text="Update Product", command=lambda: controller.switch_frame(UpdateProduct)).pack()
        tk.Button(self, text="Main Menu", command=lambda: controller.switch_frame(MainMenu)).pack()
        tk.Button(self, text="Quit", command=self.quit).pack()

    def quit(self):
        self.controller.master.quit()

class AddProduct(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        tk.Label(self, text="Add Product").pack()
        tk.Label(self, text="Product Name").pack()
        self.product_name_entry = tk.Entry(self)
        self.product_name_entry.pack()
        tk.Label(self, text="Price").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()
        tk.Label(self, text="Emoji").pack()
        self.emoji_entry = tk.Entry(self)
        self.emoji_entry.pack()
        tk.Button(self, text="Add", command=self.add_product).pack()
        tk.Button(self, text="Admin Menu", command=lambda: controller.switch_frame(AdminMenu)).pack()

    def add_product(self):
        product_name = self.product_name_entry.get()
        price = self.price_entry.get()
        emoji = self.emoji_entry.get()
        self.controller.data_manager.add_or_update_product(product_name, price, emoji)

class UpdateProduct(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        tk.Label(self, text="Update Product").pack()
        tk.Label(self, text="Product Name").pack()
        self.product_name_entry = tk.Entry(self)
        self.product_name_entry.pack()
        tk.Label(self, text="Price").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()
        tk.Label(self, text="Emoji").pack()
        self.emoji_entry = tk.Entry(self)
        self.emoji_entry.pack()
        tk.Button(self, text="Update", command=self.update_product).pack()
        tk.Button(self, text="Admin Menu", command=lambda: controller.switch_frame(AdminMenu)).pack()

    def update_product(self):
        product_name = self.product_name_entry.get()
        price = self.price_entry.get()
        emoji = self.emoji_entry.get()
        self.controller.data_manager.add_or_update_product(product_name, price, emoji)

class ProductSelection(BaseFrame):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        products = controller.data_manager.get_products()
        for product in products:
            tk.Label(self, text=f"{product['name']} - {product['price']} - {product['emoji']}").pack()

        tk.Button(self, text="Main Menu", command=lambda: controller.switch_frame(MainMenu)).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root, 'data.json')
    app.run()