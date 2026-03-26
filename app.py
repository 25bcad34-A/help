from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database connection (Railway compatible)
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST", "localhost"),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", ""),
    database=os.getenv("MYSQLDATABASE", "portfolio"),
    port=int(os.getenv("MYSQLPORT"))

)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT
)
""")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)