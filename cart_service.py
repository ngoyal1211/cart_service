from flask import Flask, jsonify, request
import requests  # To make HTTP requests to the Product Service

app = Flask(__name__)

product_service_url = "http://127.0.0.1/products" 

response = requests.get(product_service_url)

if response.status_code == 200:
    products = response.json()
    print("Products from Product Service:")
    for product in products:
        print(product)
else:
    print("Error:", response.status_code)

# Simulate cart contents
carts = [
    {
        "user_id": 1,
        "items": [
            {
               "product_id": None,
               "price": None,
               "quantity": None
            },

            {
                "product_id": None,
                "price": None,
                "quantity": None
            }
        ]
    },
    {
        "user_id": 2,
        "items": [
            {
                "product_id": None,
                "price": None,
                "quantity": None
            },
            {
                "product_id": None,
                "price": None,
                "quantity": None
            }
        ]
    },
]

# Retrieve the current contents of a user's shopping cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    # Simulate interacting with the Product Service to get cart contents
    product_service_url = fhttp://127.0.0.1/products"
    response = requests.get(product_service_url)
    products = response.json()


    # Calculate total prices
    cart_details = []
    for item in cart_contents:
        product_id = item["product_id"]
        product = next((p for p in products if p["id"] == product_id), None)
        if product is not None:
            total_price = product["price"] * item["quantity"]
            cart_details.append({
                "product_id": product_id,
                "name": product["name"],
                "quantity": item["quantity"],
                "total_price": total_price,
            })

    return jsonify(cart_details)

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)

    # Retrieve product information from the Product Service
    product_response = requests.get(f"{product_service_url}/products/{product_id}")
    
    if product_response.status_code == 200:
        product = product_response.json()
        product_name = product['name']
        product_price = product['price']
        
        if user_id < len(carts):
            cart = carts[user_id]
            product_index = next((i for i, item in enumerate(cart) if item['product_id'] == product_id), None)

            if product_index is not None:
                # Product is already in the cart, increase the quantity
                cart[product_index]['quantity'] += quantity
            else:
                # Product is not in the cart, add it
                cart.append({"product_id": product_id, "quantity": quantity})
            return jsonify({"message": f"Added {quantity} {product_name}(s) to cart"}), 201
        return jsonify({"error": "User not found"}), 404
    return jsonify({"error": "Product not found"}), 404

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)

    # Retrieve product information from the Product Service
    product_response = requests.get(f"{product_service_url}/products/{product_id}")

    if product_response.status_code == 200:
        product = product_response.json()
        product_name = product['name']

        if user_id < len(carts):
            cart = carts[user_id]
            product_index = next((i for i, item in enumerate(cart) if item['product_id'] == product_id), None)

            if product_index is not None:
                # Product is in the cart, decrease the quantity
                cart_item = cart[product_index]
                cart_item['quantity'] -= quantity

                # Remove the item if the quantity is zero or negative
                if cart_item['quantity'] <= 0:
                    cart.pop(product_index)
                return jsonify({"message": f"Removed {quantity} {product_name}(s) from cart"}), 200
            return jsonify({"error": "Product not found in the cart"}), 404
        return jsonify({"error": "User not found"}), 404
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
