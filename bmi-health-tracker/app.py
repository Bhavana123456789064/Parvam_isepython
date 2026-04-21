from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import date

app = Flask(__name__)

DATA_FILE = "health.json"


def load_records():
    if not os.path.exists(DATA_FILE):
        return {"records": []}
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            if "records" not in data:
                return {"records": []}
            return data
        except json.JSONDecodeError:
            return {"records": []}


def save_records(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


@app.route("/")
def index():
    data = load_records()
    return render_template("index.html", records=data["records"])


@app.route("/save", methods=["POST"])
def save():
    payload = request.get_json()
    name = payload.get("name", "").strip()
    age = payload.get("age")
    weight = payload.get("weight")
    height = payload.get("height")

    if not name or not age or not weight or not height:
        return jsonify({"error": "All fields are required"}), 400

    try:
        age = int(age)
        weight = float(weight)
        height = float(height)
    except ValueError:
        return jsonify({"error": "Invalid numeric values"}), 400

    bmi = round(weight / (height ** 2) * 10000, 1)
    category = get_category(bmi)

    data = load_records()
    existing = data["records"]
    new_id = (max(r["id"] for r in existing) + 1) if existing else 1

    record = {
        "id": new_id,
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "category": category,
        "date": str(date.today())
    }

    existing.append(record)
    save_records(data)

    return jsonify({"success": True, "record": record})


@app.route("/records")
def records():
    data = load_records()
    return jsonify(data["records"])


if __name__ == "__main__":
    # Start with empty JSON if file doesn't exist
    if not os.path.exists(DATA_FILE):
        save_records({"records": []})
        print("✅ Created empty health.json")
    app.run(debug=True)