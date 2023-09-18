from flask import Flask, render_template, request, jsonify
# from src.db import get_db_connection, return_db_connection


app = Flask(__name__)

@app.route('/')
def index():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    
    # cursor.execute("SELECT 'hola mundo';")
    # records = cursor.fetchall()

    # return_db_connection(conn)
    records = "hola mundo"
    return render_template('index.html', records=records)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    # Aquí puedes procesar los datos del formulario como desees.
    return jsonify({"message": "Formulario recibido!", "name": name, "email": email})

if __name__ == "__main__":
    app.run(debug=True)

