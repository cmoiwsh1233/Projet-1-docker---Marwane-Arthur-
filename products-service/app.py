from datetime import date

from flask import Flask, jsonify, request


app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "stock": 10,
        "created_at": "2026-03-13",
    }
]
next_id = 2


def json_error(message, status_code):
    return jsonify({"error": message}), status_code


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/products")
def get_products():
    return jsonify(products)


@app.get("/products/<int:product_id>")
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return json_error("Product not found", 404)


@app.post("/products")
def create_product():
    global next_id

    payload = request.get_json(silent=True)
    if not payload:
        return json_error("Invalid JSON body", 400)

    required_fields = ["name", "price", "stock"]
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        return json_error(f"Missing fields: {', '.join(missing_fields)}", 400)

    product = {
        "id": next_id,
        "name": payload["name"],
        "price": payload["price"],
        "stock": payload["stock"],
        "created_at": str(date.today()),
    }
    products.append(product)
    next_id += 1
    return jsonify(product), 201


@app.put("/products/<int:product_id>")
def update_product(product_id):
    payload = request.get_json(silent=True)
    if not payload:
        return json_error("Invalid JSON body", 400)

    for product in products:
        if product["id"] == product_id:
            for field in ["name", "price", "stock"]:
                if field in payload:
                    product[field] = payload[field]
            return jsonify(product)

    return json_error("Product not found", 404)


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(index)
            return jsonify(deleted_product)
    return json_error("Product not found", 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
