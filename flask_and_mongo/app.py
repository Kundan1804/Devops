from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import json
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Needed for flash messages

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://kundanagrawal18:removed_it_cluster0.jfywelg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true")
db = client["practicedb"]
collection = db["users"]

@app.route('/api')
def get_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success'))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return render_template('form.html')
    return render_template('form.html')

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    try:
        item_name = request.form['itemName']
        item_desc = request.form['itemDescription']
        collection.insert_one({"item_name": item_name, "item_description": item_desc})
        return jsonify({"status": "success", "message": "Item added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/todo', methods=['GET'])
def todo_form():
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(debug=True)
