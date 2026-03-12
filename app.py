import pickle
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    probability = None

    if request.method == "POST":

        gpa = float(request.form["gpa"])
        coding = int(request.form["coding"])
        ml_skill = int(request.form["ml_skill"])
        internship = int(request.form["internship"])

        data = pd.DataFrame([[gpa, coding, ml_skill, internship]],
                            columns=["gpa", "coding", "ml_skill", "internship"])

        prediction = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        probability = round(prob * 100, 2)

        if prediction == 1:
            result = "High chances of placement!"
        else:
            result = "Needs improvement for placement."

    return render_template("index.html", result=result, probability=probability)


# REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        gpa = request.form["gpa"]
        coding = request.form["coding"]
        ml_skill = request.form["ml_skill"]
        internship = request.form["internship"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO users (name,email,password,gpa,coding,ml_skill,internship) VALUES (?,?,?,?,?,?,?)",
        (name,email,password,gpa,coding,ml_skill,internship)
        )

        conn.commit()
        conn.close()

        return "Registration Successful"

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:

            gpa = user[4]
            coding = user[5]
            ml_skill = user[6]
            internship = user[7]

            data = pd.DataFrame([[gpa, coding, ml_skill, internship]],
                                columns=["gpa", "coding", "ml_skill", "internship"])

            prob = model.predict_proba(data)[0][1]
            probability = round(prob * 100, 2)

            strengths = []
            weaknesses = []
            suggestions = []

            if gpa >= 8:
                strengths.append("Strong academic performance")
            else:
                weaknesses.append("Low GPA")
                suggestions.append("Focus on improving academics")

            if coding >= 200:
                strengths.append("Good coding practice")
            else:
                weaknesses.append("Low coding practice")
                suggestions.append("Solve at least 200 coding problems")

            if ml_skill == 1:
                strengths.append("ML knowledge present")
            else:
                weaknesses.append("No ML knowledge")
                suggestions.append("Learn basics of Machine Learning")

            if internship >= 1:
                strengths.append("Has internship experience")
            else:
                weaknesses.append("No internship experience")
                suggestions.append("Apply for internships")

            return render_template(
                "dashboard.html",
                user=user,
                probability=probability,
                strengths=strengths,
                weaknesses=weaknesses,
                suggestions=suggestions
            )

        else:
            return "Invalid login"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    user = cursor.fetchone()

    conn.close()

    gpa = user[4]
    coding = user[5]
    ml_skill = user[6]
    internship = user[7]

    data = pd.DataFrame([[gpa, coding, ml_skill, internship]],
                        columns=["gpa","coding","ml_skill","internship"])

    prob = model.predict_proba(data)[0][1]
    probability = round(prob * 100, 2)

    strengths = []
    weaknesses = []
    suggestions = []

    if gpa >= 8:
        strengths.append("Strong academic performance")
    else:
        weaknesses.append("Low GPA")
        suggestions.append("Focus on improving academics")

    if coding >= 200:
        strengths.append("Good coding practice")
    else:
        weaknesses.append("Low coding practice")
        suggestions.append("Solve at least 200 coding problems")

    if ml_skill == 1:
        strengths.append("ML knowledge present")
    else:
        weaknesses.append("No ML knowledge")
        suggestions.append("Learn basics of Machine Learning")

    if internship >= 1:
        strengths.append("Has internship experience")
    else:
        weaknesses.append("No internship experience")
        suggestions.append("Apply for internships")

    return render_template(
        "dashboard.html",
        user=user,
        probability=probability,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions
    )
@app.route("/logout")
def logout():
    return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(debug=True)