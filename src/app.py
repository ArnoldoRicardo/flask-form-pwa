import logging

from flask import Flask, abort, jsonify, render_template, request
from flask_bootstrap import Bootstrap4

from src.crud import get_all_expenses, insert_expense
from src.schemas import Expense

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    Bootstrap4(app)
    return app


app = create_app()


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify(error="Internal server error"), 500


@app.route('/')
def index():
    try:
        records = get_all_expenses()
        return render_template('index.html', records=records)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
        abort(500)


@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        expense = Expense(
            total=request.form.get('total'),
            note=request.form.get('note'),
            date=request.form.get('date')
        )
        saved = insert_expense(expense)
        if saved:
            return jsonify(expense.dict())
    except ValueError as e:
        logger.error(f"Bad request: {e}")
        abort(400)
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)
