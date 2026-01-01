from flask import Flask, render_template, request, redirect, session
from questions import questions

app = Flask(__name__)
app.secret_key = "finalyearproject"

leaderboard = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["name"] = request.form["name"]
        return redirect("/subjects")
    return render_template("index.html")

@app.route("/subjects")
def subjects():
    return render_template("subjects.html", subjects=questions.keys())

@app.route("/quiz/<subject>", methods=["GET", "POST"])
def quiz(subject):
    if "qno" not in session:
        session["qno"] = 0
        session["score"] = 0
        session["subject"] = subject

    qlist = questions[subject]

    if request.method == "POST":
        selected = request.form.get("answer")
        if selected == qlist[session["qno"]]["answer"]:
            session["score"] += 1
        session["qno"] += 1

        if session["qno"] >= len(qlist):
            leaderboard.append({
                "name": session["name"],
                "subject": subject,
                "score": session["score"]
            })
            session.clear()
            return redirect("/leaderboard")

    return render_template(
        "quiz.html",
        question=qlist[session["qno"]],
        score=session["score"],
        subject=subject
    )

@app.route("/leaderboard")
def show_leaderboard():
    return render_template("leaderboard.html", leaderboard=leaderboard)

app.run(debug=True)
