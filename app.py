from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import csv
from datetime import datetime
import os

app = Flask(__name__)

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS work_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_name TEXT NOT NULL,
            task TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            work_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save-session", methods=["POST"])
def save_session():
    data = request.json

    manager_name = data["manager_name"]
    task = data["task"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    duration_minutes = data["duration_minutes"]
    work_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO work_sessions 
        (manager_name, task, start_time, end_time, duration_minutes, work_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (manager_name, task, start_time, end_time, duration_minutes, work_date))

    conn.commit()
    conn.close()

    return jsonify({"message": "Work session saved successfully"})


@app.route("/sessions")
def get_sessions():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM work_sessions ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    sessions = []
    for row in rows:
        sessions.append({
            "id": row[0],
            "manager_name": row[1],
            "task": row[2],
            "start_time": row[3],
            "end_time": row[4],
            "duration_minutes": row[5],
            "work_date": row[6]
        })

    return jsonify(sessions)


@app.route("/export")
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT manager_name, task, start_time, end_time, duration_minutes, work_date FROM work_sessions")
    rows = cur.fetchall()
    conn.close()

    filename = "work_hours_report.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Manager Name", "Task", "Start Time", "End Time", "Duration Minutes", "Date"])
        writer.writerows(rows)

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)