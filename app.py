from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

config = {
    'user': 'root',  # Replace 'root' with your MySQL username
    'password': '1234',  # Replace 'password' with your MySQL password
    'host': 'localhost',
    'database': 'todo_db',  # Make sure this database exists or create it
    'raise_on_warnings': True
}

def get_db_connection():
    conn = mysql.connector.connect(**config)
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SHOW TABLES LIKE 'tasks' ''')
    if cursor.fetchone() is None:
        cursor.execute('''CREATE TABLE tasks
                          (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))''')
        conn.commit()
    conn.close()



@app.route('/')
def index():
    create_table()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)