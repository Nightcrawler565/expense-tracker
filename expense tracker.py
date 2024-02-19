from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = 'expenses.db'


# Database initialization and connection handling

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Routes

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    return render_template('index.html', expenses=expenses)


@app.route('/add', methods=['POST'])
def add_expenses():
    date = request.form['date']
    amount = float(request.form['amount'])
    category=request.form['category']
    description=request.form['description']

    db= get_db()
    db.execute('INSERT INTO expenses (date,amount,category,description) VALUES (?,?,?,?)',[date,amount,category,description])
    db.commit()

    return redirect(url_for('index'))

@app.route('/statistics')
def statistics():
    db=get_db()
    cursor=db.execute('SELECT category,SUM(amount) as total FROM expenses GROUP BY category')
    category_totals=cursor.fetchall()

    return render_template('statistics.html',category_totals=category_totals)

if __name__=='__main__':
    app.run(debug=True)
