from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from risk_report import generate_risk_report

app = Flask(__name__)

CORS(app)

voters = pd.read_csv("dataset/cleaned_voters.csv")


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/verification")
def verification():
    return render_template("verification.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/voters")
def get_voters():
    return jsonify(
        voters.to_dict(orient="records")
    )


@app.route("/risk-report")
def risk_report():
    return jsonify(
        generate_risk_report()
    )


if __name__ == "__main__":
    app.run(debug=True)