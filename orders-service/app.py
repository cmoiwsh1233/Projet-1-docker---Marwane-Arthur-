from datetime import date

import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

PRODUCTS_SERVICE_URL = "http://products-service:5002/products"

orders = []
next_id = 1


def json_error(message, status_code):
    return jsonify({"error": message}), status_code


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/orders")
def get_orders():
    return jsonify(orders)


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            return jsonify(order)
    return json_error("Order not found", 404)


@app.get("/orders/user/<int:user_id>")
def get_orders_by_user(user_id):
    user_orders = [order for order in orders if order["user_id"] == user_id]
    return jsonify(user_orders)


@app.post("/orders")
def create_order():
    global next_id

    payload = request.get_json(silent=True)
    if not payload:
        return json_error("Invalid JSON body", 400)

    required_fields = ["user_id", "product_id", "quantity"]
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        return json_error(f"Missing fields: {', '.join(missing_fields)}", 400)

    quantity = payload["quantity"]
    if not isinstance(quantity, int) or quantity <= 0:
        return json_error("Quantity must be a positive integer", 400)

    product_id = payload["product_id"]

    try:
        response = requests.get(f"{PRODUCTS_SERVICE_URL}/{product_id}", timeout=5)
    except requests.RequestException:
        return json_error("Products service unavailable", 503)

    if response.status_code == 404:
        return json_error("Product not found", 404)
    if not response.ok:
        return json_error("Unable to verify product", 502)

    product = response.json()
    stock = product.get("stock")
    price = product.get("price")

    if stock is None or price is None:
        return json_error("Invalid product data received", 502)
    if stock < quantity:
        return json_error("Insufficient stock", 400)

    order = {
        "id": next_id,
        "user_id": payload["user_id"],
        "product_id": product_id,
        "quantity": quantity,
        "total_price": price * quantity,
        "status": "created",
        "created_at": str(date.today()),
    }
    orders.append(order)
    next_id += 1
    return jsonify(order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
