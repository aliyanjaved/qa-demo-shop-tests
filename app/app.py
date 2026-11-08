"""Demo web shop used as the system under test (SUT).

It exposes a small REST API and a server-rendered UI (login, product list, cart,
checkout). Three defects can be switched on with SEEDED_BUGS=true so the test
suite has something real to catch (see docs/defect_reports.md).
"""
import os
import uuid

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "demo-only-secret"

SEEDED_BUGS = os.getenv("SEEDED_BUGS", "false").lower() == "true"

USERS = {"standard_user": "secret123", "locked_user": "secret123"}
LOCKED = {"locked_user"}
PRODUCTS = [
    {"id": 1, "name": "Backpack", "price": 29.99, "stock": 10},
    {"id": 2, "name": "Bike Light", "price": 9.99, "stock": 25},
    {"id": 3, "name": "Water Bottle", "price": 12.50, "stock": 40},
    {"id": 4, "name": "Fleece Jacket", "price": 49.00, "stock": 5},
    {"id": 5, "name": "Trail Shoes", "price": 89.90, "stock": 8},
    {"id": 6, "name": "Sun Hat", "price": 15.00, "stock": 12},
]
TOKENS = {}        # token -> username
API_CARTS = {}     # token -> {product_id: quantity}
ORDERS = []


def find_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)


def search(q):
    q = (q or "").strip()
    if not q:
        return list(PRODUCTS)
    if SEEDED_BUGS:  # BUG-001: search is case sensitive
        return [p for p in PRODUCTS if q in p["name"]]
    return [p for p in PRODUCTS if q.lower() in p["name"].lower()]


def cart_lines(cart):
    lines = []
    for pid, qty in cart.items():
        p = find_product(int(pid))
        lines.append({"product_id": p["id"], "name": p["name"], "price": p["price"],
                      "quantity": qty})
    return lines


def cart_total(cart):
    total = 0.0
    for line in cart_lines(cart):
        if SEEDED_BUGS:  # BUG-002: quantity is ignored in the total
            total += line["price"]
        else:
            total += line["price"] * line["quantity"]
    return round(total, 2)


def valid_checkout(name, address):
    if not name or not name.strip():
        return False
    if SEEDED_BUGS:  # BUG-003: empty address is accepted
        return True
    return bool(address and address.strip())


# ------------------------------------------------------------------ REST API
def api_user():
    header = request.headers.get("Authorization", "")
    token = header.replace("Bearer ", "", 1) if header.startswith("Bearer ") else None
    return token if token in TOKENS else None


@app.post("/api/login")
def api_login():
    data = request.get_json(silent=True) or {}
    username, password = data.get("username"), data.get("password")
    if not username or not password:
        return jsonify(error="username and password are required"), 400
    if username in LOCKED and USERS.get(username) == password:
        return jsonify(error="user is locked out"), 423
    if USERS.get(username) != password:
        return jsonify(error="invalid credentials"), 401
    token = str(uuid.uuid4())
    TOKENS[token] = username
    return jsonify(token=token), 200


@app.get("/api/products")
def api_products():
    return jsonify(products=search(request.args.get("q"))), 200


@app.get("/api/products/<int:pid>")
def api_product(pid):
    p = find_product(pid)
    return (jsonify(p), 200) if p else (jsonify(error="product not found"), 404)


@app.post("/api/cart")
def api_cart_add():
    token = api_user()
    if not token:
        return jsonify(error="unauthorized"), 401
    data = request.get_json(silent=True) or {}
    pid, qty = data.get("product_id"), data.get("quantity", 1)
    p = find_product(pid) if isinstance(pid, int) else None
    if not p:
        return jsonify(error="product not found"), 404
    if not isinstance(qty, int) or qty < 1:
        return jsonify(error="quantity must be a positive integer"), 400
    cart = API_CARTS.setdefault(token, {})
    if cart.get(str(pid), 0) + qty > p["stock"]:
        return jsonify(error="not enough stock"), 409
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    return jsonify(items=cart_lines(cart), total=cart_total(cart)), 201


@app.get("/api/cart")
def api_cart_get():
    token = api_user()
    if not token:
        return jsonify(error="unauthorized"), 401
    cart = API_CARTS.get(token, {})
    return jsonify(items=cart_lines(cart), total=cart_total(cart)), 200


@app.post("/api/checkout")
def api_checkout():
    token = api_user()
    if not token:
        return jsonify(error="unauthorized"), 401
    cart = API_CARTS.get(token, {})
    if not cart:
        return jsonify(error="cart is empty"), 400
    data = request.get_json(silent=True) or {}
    if not valid_checkout(data.get("name"), data.get("address")):
        return jsonify(error="name and address are required"), 400
    order = {"order_id": len(ORDERS) + 1001, "total": cart_total(cart)}
    ORDERS.append(order)
    API_CARTS[token] = {}
    return jsonify(order), 201


@app.post("/api/test/reset")
def api_reset():
    TOKENS.clear(); API_CARTS.clear(); ORDERS.clear()
    return jsonify(status="reset"), 200


@app.get("/health")
def health():
    return jsonify(status="ok", seeded_bugs=SEEDED_BUGS), 200


# ------------------------------------------------------------------------ UI
def ui_cart():
    return session.setdefault("cart", {})


@app.route("/")
def index():
    return redirect(url_for("products" if session.get("user") else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u, p = request.form.get("username", ""), request.form.get("password", "")
        if not u or not p:
            error = "Username and password are required"
        elif u in LOCKED and USERS.get(u) == p:
            error = "This user is locked out"
        elif USERS.get(u) != p:
            error = "Invalid credentials"
        else:
            session["user"] = u
            return redirect(url_for("products"))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/products")
def products():
    if not session.get("user"):
        return redirect(url_for("login"))
    q = request.args.get("q", "")
    count = sum(ui_cart().values())
    return render_template("products.html", products=search(q), q=q, count=count)


@app.post("/cart/add/<int:pid>")
def cart_add(pid):
    cart = ui_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session.modified = True
    return redirect(request.referrer or url_for("products"))


@app.post("/cart/remove/<int:pid>")
def cart_remove(pid):
    ui_cart().pop(str(pid), None)
    session.modified = True
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    if not session.get("user"):
        return redirect(url_for("login"))
    c = ui_cart()
    return render_template("cart.html", lines=cart_lines(c), total=cart_total(c))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get("user"):
        return redirect(url_for("login"))
    error, order = None, None
    c = ui_cart()
    if request.method == "POST":
        if not c:
            error = "Your cart is empty"
        elif not valid_checkout(request.form.get("name"), request.form.get("address")):
            error = "Name and address are required"
        else:
            order = {"order_id": len(ORDERS) + 1001, "total": cart_total(c)}
            ORDERS.append(order)
            session["cart"] = {}
    return render_template("checkout.html", error=error, order=order, total=cart_total(c))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
