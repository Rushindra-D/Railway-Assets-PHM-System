from flask import Flask, render_template
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

def get_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database", "phm_data.db")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM rul_results", conn)
    conn.close()

    df = df.sort_values(by="File").reset_index(drop=True)
    return df


# HOME
@app.route("/")
def home():
    return render_template("home.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    df = get_data()
    latest = df.iloc[-1]

    health = latest["Health_Index"]
    rul = latest["Estimated_RUL"]

    # Status
    if health > 0.7:
        status = "Healthy"
    elif health > 0.4:
        status = "Warning"
    else:
        status = "Critical"

    return render_template(
        "dashboard.html",
        health=round(health, 3),
        rul=int(rul),
        total=len(df),
        status=status,
        files=df["File"].tolist()[-50:],  # last 50 points
        health_data=df["Health_Index"].tolist()[-50:],
        rul_data=df["Estimated_RUL"].tolist()[-50:],
        avg_health=round(df["Health_Index"].mean(), 3),
        avg_rul=int(df["Estimated_RUL"].mean())
    )


# HEALTH PAGE
@app.route("/health")
def health():
    df = get_data()
    latest = df.iloc[-1]

    health_val = latest["Health_Index"]

    # Status logic
    if health_val > 0.7:
        status = "Healthy"
    elif health_val > 0.4:
        status = "Warning"
    else:
        status = "Critical"

    return render_template(
        "health.html",
        files=df["File"].tolist(),
        health_data=df["Health_Index"].tolist(),
        current_health=round(health_val, 3),
        status=status,
        avg_health=round(df["Health_Index"].mean(), 3),
        min_health=round(df["Health_Index"].min(), 3),
        max_health=round(df["Health_Index"].max(), 3)
    )


# RUL PAGE
@app.route("/rul")
def rul():
    df = get_data()
    latest = df.iloc[-1]

    return render_template(
        "rul.html",
        files=df["File"].tolist(),
        rul_data=df["Estimated_RUL"].tolist(),
        current_rul=int(latest["Estimated_RUL"]),
        avg_rul=int(df["Estimated_RUL"].mean()),
        min_rul=int(df["Estimated_RUL"].min()),
        max_rul=int(df["Estimated_RUL"].max())
    )


# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)