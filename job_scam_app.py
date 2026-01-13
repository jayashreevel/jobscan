from flask import Flask, request, render_template
import joblib
import sqlite3
from datetime import datetime

app = Flask(__name__)

model = joblib.load("job_scam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/", methods=["GET", "POST"])
def detect():
    result = ""
    job_url = ""

    if request.method == "POST":
        job_url = request.form["url"]
        job_title = request.form["title"]
        job_desc = request.form["description"]

        combined_text = job_title + " " + job_desc
        vec = vectorizer.transform([combined_text])
        pred = model.predict(vec)[0]

        result = "⚠️ Scam Job Posting" if pred == 1 else "✅ Legitimate Job Posting"

        conn = sqlite3.connect("job_results.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO results (job_title, job_description, job_url, prediction, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            job_title,
            job_desc,
            job_url,
            result,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    return render_template("index.html", result=result, url=job_url)

if __name__ == "__main__":
    app.run()
