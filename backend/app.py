"""
ENSF 381 - Assignment 4
Group Members:
1. Your Name - UCID
2. Your Partner Name - UCID
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import json
import os
import random
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAVORS_FILE = os.path.join(BASE_DIR, "flavors.json")
REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")


# Load JSON data

def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []

flavors = load_json_file(FLAVORS_FILE)
reviews = load_json_file(REVIEWS_FILE)


# In-memory users

users = [
    {
        "id": 1,
        "username": "demoUser",
        "email": "demo@example.com",
        "password_hash": bcrypt.hashpw("DemoPass!1".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "cart": [],
        "orders": []
    }
]

next_user_id = 2
next_order_id = 1

# Helper functions
def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def get_user_by_username(username):
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None

def get_user_by_email(email):
    for user in users:
        if user["email"].lower() == email.lower():
            return user
    return None

def get_flavor_by_id(flavor_id):
    for flavor in flavors:
        if flavor["id"] == flavor_id:
            return flavor
    return None

def get_cart_item(user, flavor_id):
    for item in user["cart"]:
        if item["flavorId"] == flavor_id:
            return item
    return None

def price_to_float(price):
    if isinstance(price, (int, float)):
        return float(price)
    return float(str(price).replace("$", "").strip())

def valid_username(username):
    if len(username) < 3 or len(username) > 20:
        return False
    return re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", username) is not None

def valid_email(email):
    return re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email) is not None

def valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Sweet Scoop backend is running."
    })


# Signup API
@app.route("/signup", methods=["POST"])
def signup():
    global next_user_id

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirmPassword", "")

    if not valid_username(username):
        return jsonify({
            "success": False,
            "message": "Username must be 3-20 characters, start with a letter, and contain only letters, numbers, underscores, and hyphens."
        }), 400

    if not valid_email(email):
        return jsonify({
            "success": False,
            "message": "Email must be in a valid format."
        }), 400

    if not valid_password(password):
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
        }), 400

    if confirm_password != "" and password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Confirm password does not match password."
        }), 400

    if get_user_by_username(username):
        return jsonify({
            "success": False,
            "message": "Username is already taken."
        }), 400

    if get_user_by_email(email):
        return jsonify({
            "success": False,
            "message": "Email is already registered."
        }), 400

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = {
        "id": next_user_id,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "cart": [],
        "orders": []
    }

    users.append(new_user)
    next_user_id += 1

    return jsonify({
        "success": True,
        "message": "Registration successful."
    }), 201


# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = get_user_by_username(username)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid username or password."
        }), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({
            "success": False,
            "message": "Invalid username or password."
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "userId": user["id"],
        "username": user["username"]
    })


# Reviews API

@app.route("/reviews", methods=["GET"])
def get_reviews():
    random_reviews = random.sample(reviews, min(2, len(reviews)))
    return jsonify({
        "success": True,
        "message": "Reviews loaded.",
        "reviews": random_reviews
    })


# Flavors API
@app.route("/flavors", methods=["GET"])
def get_flavors():
    return jsonify({
        "success": True,
        "message": "Flavors loaded.",
        "flavors": flavors
    })


# Get cart API
@app.route("/cart", methods=["GET"])
def get_cart():
    user_id = request.args.get("userId", type=int)
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Cart loaded.",
        "cart": user["cart"]
    })


# Add to cart API
@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    user_id = data.get("userId")
    flavor_id = data.get("flavorId")

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    flavor = get_flavor_by_id(flavor_id)
    if not flavor:
        return jsonify({"success": False, "message": "Flavor not found."}), 404

    if get_cart_item(user, flavor_id):
        return jsonify({
            "success": False,
            "message": "Flavor already in cart. Use PUT /cart to update quantity."
        }), 400

    user["cart"].append({
        "flavorId": flavor["id"],
        "name": flavor["name"],
        "price": price_to_float(flavor["price"]),
        "quantity": 1
    })

    return jsonify({
        "success": True,
        "message": "Flavor added to cart.",
        "cart": user["cart"]
    }), 201


# Update cart quantity API

@app.route("/cart", methods=["PUT"])
def update_cart():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    user_id = data.get("userId")
    flavor_id = data.get("flavorId")
    quantity = data.get("quantity")

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    item = get_cart_item(user, flavor_id)
    if not item:
        return jsonify({"success": False, "message": "Flavor is not in the cart."}), 404

    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({
            "success": False,
            "message": "Quantity must be at least 1."
        }), 400

    item["quantity"] = quantity

    return jsonify({
        "success": True,
        "message": "Cart updated successfully.",
        "cart": user["cart"]
    })


# Delete cart item API

@app.route("/cart", methods=["DELETE"])
def delete_cart_item():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    user_id = data.get("userId")
    flavor_id = data.get("flavorId")

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    item = get_cart_item(user, flavor_id)
    if not item:
        return jsonify({"success": False, "message": "Flavor is not in the cart."}), 404

    user["cart"].remove(item)

    return jsonify({
        "success": True,
        "message": "Flavor removed from cart.",
        "cart": user["cart"]
    })


# Place order API

@app.route("/orders", methods=["POST"])
def place_order():
    global next_order_id

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    user_id = data.get("userId")
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    if len(user["cart"]) == 0:
        return jsonify({"success": False, "message": "Cart is empty."}), 400

    total = 0
    for item in user["cart"]:
        total += item["price"] * item["quantity"]

    order = {
        "orderId": next_order_id,
        "items": user["cart"].copy(),
        "total": round(total, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user["orders"].append(order)
    user["cart"] = []
    next_order_id += 1

    return jsonify({
        "success": True,
        "message": "Order placed successfully.",
        "orderId": order["orderId"]
    }), 201


# Order history API

@app.route("/orders", methods=["GET"])
def get_orders():
    user_id = request.args.get("userId", type=int)
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Order history loaded.",
        "orders": user["orders"]
    })

if __name__ == "__main__":
    app.run()