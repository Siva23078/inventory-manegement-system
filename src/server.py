import pymongo
import os
from database import Inventory
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()
app = Flask(__name__)

myclient = pymongo.MongoClient(os.getenv("MONGO_URI"))
my_shopping_list = myclient["shopping_list"]

inventory = Inventory(my_shopping_list)
inventory.show()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/editItems", methods = ['POST'])
def edit_items():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid data received"}), 400
    inventory.update_item(item_name=data['name'], qty=data['quantity'], item_category=data['category'], item_price=data['price'], id=data['id'], reorder_level=data['reorderLevel'])
    return jsonify({"success": True, "message": "Product updated successfully"})

@app.route("/addItems", methods = ['POST'])
def add_items():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid data received"}), 400
    inventory.add_item(item_name=data['name'], qty=data['quantity'], item_category=data['category'], item_price=data['price'], reorder_level=data['reorderLevel'])
    return jsonify({"success": True, "message": "Product added successfully"})

@app.route("/removeItems", methods = ['POST'])
def remove_items():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid data received"}), 400
    inventory.del_item(id=data['id'])
    return jsonify({"success": True, "message": "Product deleted successfully"})

@app.route("/get", methods=["GET"])
def fetch():
    return jsonify({"inventory": inventory.fetch_all()})
app.run()