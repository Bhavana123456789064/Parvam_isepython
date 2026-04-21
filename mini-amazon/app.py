from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, init_db
import os

app = Flask(__name__)
app.secret_key = "mini_amazon_secret_2025"


# ── Helpers ────────────────────────────────────────────────────────
def current_user():
    if "user_id" not in session:
        return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if not user or not user["is_admin"]:
            flash("Admin access only.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


def get_cart():
    return session.get("cart", {})


def cart_count():
    return sum(get_cart().values())


app.jinja_env.globals["cart_count"] = cart_count
app.jinja_env.globals["current_user"] = current_user


# ── Auth ───────────────────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form["name"].strip()
        email    = request.form["email"].strip()
        password = request.form["password"]
        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        db.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                   (name, email, generate_password_hash(password)))
        db.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form["email"].strip()
        password = request.form["password"]
        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


# ── Shop ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    db       = get_db()
    category = request.args.get("category", "")
    search   = request.args.get("search", "")
    query    = "SELECT * FROM products WHERE stock > 0"
    params   = []
    if category:
        query  += " AND category=?"
        params.append(category)
    if search:
        query  += " AND name LIKE ?"
        params.append(f"%{search}%")
    products   = db.execute(query, params).fetchall()
    categories = db.execute("SELECT DISTINCT category FROM products").fetchall()
    return render_template("index.html", products=products,
                           categories=categories, selected_cat=category, search=search)


@app.route("/product/<int:pid>")
def product(pid):
    db   = get_db()
    prod = db.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not prod:
        flash("Product not found.", "danger")
        return redirect(url_for("index"))
    related = db.execute("SELECT * FROM products WHERE category=? AND id!=? LIMIT 4",
                         (prod["category"], pid)).fetchall()
    return render_template("product.html", product=prod, related=related)


# ── Cart ───────────────────────────────────────────────────────────
@app.route("/cart")
def cart():
    cart_data = get_cart()
    db        = get_db()
    items     = []
    total     = 0
    for pid_str, qty in cart_data.items():
        p = db.execute("SELECT * FROM products WHERE id=?", (int(pid_str),)).fetchone()
        if p:
            subtotal = p["price"] * qty
            total   += subtotal
            items.append({"product": p, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", items=items, total=total)


@app.route("/cart/add/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    qty  = int(request.form.get("qty", 1))
    cart = session.get("cart", {})
    key  = str(pid)
    cart[key] = cart.get(key, 0) + qty
    session["cart"] = cart
    flash("Added to cart!", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    pid = request.form["pid"]
    qty = int(request.form["qty"])
    cart = session.get("cart", {})
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart/remove/<pid>")
def remove_from_cart(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    flash("Item removed.", "info")
    return redirect(url_for("cart"))


# ── Checkout ───────────────────────────────────────────────────────
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_data = get_cart()
    if not cart_data:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))

    db    = get_db()
    items = []
    total = 0
    for pid_str, qty in cart_data.items():
        p = db.execute("SELECT * FROM products WHERE id=?", (int(pid_str),)).fetchone()
        if p:
            subtotal = p["price"] * qty
            total   += subtotal
            items.append({"product": p, "qty": qty, "subtotal": subtotal})

    if request.method == "POST":
        name    = request.form["name"].strip()
        address = request.form["address"].strip()
        phone   = request.form["phone"].strip()
        # Store order details in session for payment page
        session["pending_order"] = {
            "name": name, "address": address,
            "phone": phone, "total": round(total, 2)
        }
        return redirect(url_for("payment"))

    return render_template("checkout.html", items=items, total=total)


# ── Payment ────────────────────────────────────────────────────────
@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    order = session.get("pending_order")
    if not order:
        return redirect(url_for("checkout"))

    if request.method == "POST":
        # Dummy payment — always succeeds
        cart_data = get_cart()
        db        = get_db()

        # Save order
        db.execute(
            "INSERT INTO orders (user_id,total,status,name,address,phone) VALUES (?,?,?,?,?,?)",
            (session["user_id"], order["total"], "Paid",
             order["name"], order["address"], order["phone"])
        )
        db.commit()
        oid = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Save order items & decrement stock
        for pid_str, qty in cart_data.items():
            p = db.execute("SELECT * FROM products WHERE id=?", (int(pid_str),)).fetchone()
            if p:
                db.execute(
                    "INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (?,?,?,?)",
                    (oid, p["id"], qty, p["price"])
                )
                db.execute("UPDATE products SET stock=stock-? WHERE id=?", (qty, p["id"]))

        db.commit()
        session.pop("cart", None)
        session.pop("pending_order", None)
        flash("Payment successful! 🎉", "success")
        return redirect(url_for("order_success", oid=oid))

    return render_template("payment.html", order=order)


@app.route("/order/success/<int:oid>")
@login_required
def order_success(oid):
    db    = get_db()
    order = db.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
    items = db.execute("""
        SELECT oi.*, p.name as pname FROM order_items oi
        JOIN products p ON oi.product_id=p.id
        WHERE oi.order_id=?
    """, (oid,)).fetchall()
    return render_template("order_success.html", order=order, items=items)


# ── Admin ──────────────────────────────────────────────────────────
@app.route("/admin")
@admin_required
def admin_dashboard():
    db           = get_db()
    total_orders = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    total_rev    = db.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status='Paid'").fetchone()[0]
    total_prods  = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_users  = db.execute("SELECT COUNT(*) FROM users WHERE is_admin=0").fetchone()[0]
    recent       = db.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("admin/dashboard.html",
                           total_orders=total_orders, total_rev=total_rev,
                           total_prods=total_prods, total_users=total_users,
                           recent=recent)


@app.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    db = get_db()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            db.execute(
                "INSERT INTO products (name,description,price,stock,category,image_url) VALUES (?,?,?,?,?,?)",
                (request.form["name"], request.form["description"],
                 float(request.form["price"]), int(request.form["stock"]),
                 request.form["category"], request.form["image_url"])
            )
            db.commit()
            flash("Product added!", "success")
        elif action == "delete":
            db.execute("DELETE FROM products WHERE id=?", (request.form["pid"],))
            db.commit()
            flash("Product deleted.", "info")
        elif action == "edit":
            db.execute(
                "UPDATE products SET name=?,description=?,price=?,stock=?,category=?,image_url=? WHERE id=?",
                (request.form["name"], request.form["description"],
                 float(request.form["price"]), int(request.form["stock"]),
                 request.form["category"], request.form["image_url"],
                 request.form["pid"])
            )
            db.commit()
            flash("Product updated!", "success")
        return redirect(url_for("admin_products"))
    products = db.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return render_template("admin/products.html", products=products)


@app.route("/admin/orders")
@admin_required
def admin_orders():
    db     = get_db()
    orders = db.execute("""
        SELECT o.*, u.name as uname, u.email
        FROM orders o JOIN users u ON o.user_id=u.id
        ORDER BY o.id DESC
    """).fetchall()
    return render_template("admin/orders.html", orders=orders)


@app.route("/admin/orders/update", methods=["POST"])
@admin_required
def update_order_status():
    db = get_db()
    db.execute("UPDATE orders SET status=? WHERE id=?",
               (request.form["status"], request.form["order_id"]))
    db.commit()
    flash("Order status updated.", "success")
    return redirect(url_for("admin_orders"))


# ── Run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=True)