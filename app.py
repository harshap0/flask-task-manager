from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY completed ASC, id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["content"]
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/complete/<int:id>")
def complete(id):
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()
    cursor.execute("SELECT completed FROM  tasks WHERE id = ?" ,(id,))
    row=cursor.fetchone()
    
    if row is None:
        conn.close()
        return redirect("/")

    current_status=row[0]
    new_status=0 if current_status==1 else 1
    cursor.execute("UPDATE tasks SET completed = ? WHERE id=?",
    (new_status, id)) 

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
