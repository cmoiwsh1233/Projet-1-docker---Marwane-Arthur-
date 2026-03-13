from datetime import date

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

users = []
next_id = 1


def json_error(message, status_code):
    response = jsonify({"error": message})
    response.status_code = status_code
    return response


def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)


def serialize_user(user):
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"],
    }


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([serialize_user(user) for user in users])


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user(user_id)
    if user is None:
        return json_error("User not found", 404)
    return jsonify(serialize_user(user))


@app.route("/users", methods=["POST"])
def create_user():
    global next_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return json_error("Invalid JSON body", 400)

    username = data.get("username") or data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return json_error("Fields 'username', 'email' and 'password' are required", 400)

    if any(user["email"] == email for user in users):
        return json_error("Email already exists", 409)

    user = {
        "id": next_id,
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password),
        "created_at": str(date.today()),
    }
    users.append(user)
    next_id += 1

    response = jsonify(serialize_user(user))
    response.status_code = 201
    return response


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = find_user(user_id)
    if user is None:
        return json_error("User not found", 404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return json_error("Invalid JSON body", 400)

    email = data.get("email")
    if email and any(existing["email"] == email and existing["id"] != user_id for existing in users):
        return json_error("Email already exists", 409)

    username = data.get("username") or data.get("name")
    if username:
        user["username"] = username
    if email:
        user["email"] = email
    if data.get("password"):
        user["password_hash"] = generate_password_hash(data["password"])

    return jsonify(serialize_user(user))


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = find_user(user_id)
    if user is None:
        return json_error("User not found", 404)

    users.remove(user)
    return jsonify({"message": "User deleted", "user": serialize_user(user)})


@app.route("/users/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return json_error("Invalid JSON body", 400)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return json_error("Fields 'email' and 'password' are required", 400)

    user = next(
        (
            stored_user
            for stored_user in users
            if stored_user["email"] == email and check_password_hash(stored_user["password_hash"], password)
        ),
        None,
    )
    if user is None:
        return json_error("Invalid credentials", 401)

    return jsonify(
        {
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"],
            },
        }
    )


@app.errorhandler(404)
def not_found(_error):
    return json_error("Route not found", 404)


@app.errorhandler(405)
def method_not_allowed(_error):
    return json_error("Method not allowed", 405)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
