import logging
from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)


logging.basicConfig(filename="error.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")


db = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="nikhil26",
    database="contact_form"
)
cursor = db.cursor()


@app.route('/')
def home():
    return render_template("home.html")   

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"error": "Name, email, and message are required"}), 400

        query = """INSERT INTO contacts (name, email, phone, subject, message) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (name, email, phone, subject, message)
        cursor.execute(query, values)
        db.commit()

        return jsonify({"success": "Message received!"}), 200

    except Exception as e:
        logging.error("Error in /submit route: %s", str(e))
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
