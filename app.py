from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Absolute database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# 🔥 Always initialize DB when app loads
init_db()


@app.route("/")
def index():
    conn = get_connection()
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY completed ASC, id DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task = request.form["content"]
    conn = get_connection()
    conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):
    conn = get_connection()
    task = conn.execute(
        "SELECT completed FROM tasks WHERE id = ?", (id,)
    ).fetchone()

    if task:
        new_status = 0 if task["completed"] == 1 else 1
        conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (new_status, id)
        )
        conn.commit()

    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
