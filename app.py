from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Example schedule
sessions = [
    {"name": "Planet Fitness", "time": "6:00 AM - 7:00 AM", "slots": 5},
    {"name": "Crunch Fitness", "time": "7:30 AM - 8:30 AM", "slots": 10},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html", sessions=sessions)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        session_name = request.form["session_name"]
        time = request.form["time"]
        slots = int(request.form["slots"])
        sessions.append({"name": session_name, "time": time, "slots": slots})
        return redirect(url_for("admin"))
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
