import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/schedule")
def schedule():
    # Connect to the database
    conn = sqlite3.connect('gym_schedule.db')
    cursor = conn.cursor()

    # Fetch schedule data
    cursor.execute("SELECT time_slot, availability FROM schedule")
    schedule_data = cursor.fetchall()

    conn.close()

    return render_template("schedule.html", schedule=schedule_data)

@app.route("/view_db")
def view_db():
    conn = sqlite3.connect('gym_schedule.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()
    conn.close()

    # Render as an HTML table
    html = "<h1>Database Contents</h1><table border='1'><tr><th>ID</th><th>Time Slot</th><th>Availability</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html += "</table>"
    return html

from flask import request

@app.route("/book_slot", methods=["POST"])
def book_slot():
    time_slot = request.form["time_slot"]

    # Update availability in the database
    conn = sqlite3.connect('gym_schedule.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE schedule SET availability = ? WHERE time_slot = ?", ('Full', time_slot))
    conn.commit()
    conn.close()

    return f"Successfully booked {time_slot}. <a href='/schedule'>Back to Schedule</a>"

@app.route("/admin")
def admin():
    conn = sqlite3.connect('gym_schedule.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule")
    schedule_data = cursor.fetchall()
    conn.close()
    return render_template("admin.html", schedule=schedule_data)


@app.route("/edit_slot/<int:id>", methods=["GET", "POST"])
def edit_slot(id):
    conn = sqlite3.connect('gym_schedule.db')
    cursor = conn.cursor()

    if request.method == "POST":
        new_availability = request.form["availability"]
        cursor.execute("UPDATE schedule SET availability = ? WHERE id = ?", (new_availability, id))
        conn.commit()
        conn.close()
        return f"Successfully updated. <a href='/admin'>Back to Admin Panel</a>"

    cursor.execute("SELECT * FROM schedule WHERE id = ?", (id,))
    slot = cursor.fetchone()
    conn.close()

    return render_template("edit_slot.html", slot=slot)



if __name__ == "__main__":
    app.run(debug=True)
