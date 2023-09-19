from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap4

from src.crud import get_all_expenses, insert_expense

app = Flask(__name__)
Bootstrap4(app)


@app.route('/')
def index():
    records = get_all_expenses()
    return render_template('index.html', records=records)


@ app.route('/submit-form', methods=['POST'])
def submit_form():
    total = request.form.get('total')
    note = request.form.get('note')
    saved = insert_expense(total, note)
    if saved:
        return jsonify({"message": "Formulario recibido!", "total": total, "note":
                        note, 'date': '2021-01-01'})


if __name__ == "__main__":
    app.run(debug=True)
