# job_scam_app.py

from flask import Flask, request, render_template_string
import joblib
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Load the trained model and text vectorizer
model = joblib.load("job_scam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# HTML Template
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CyberShield_Her 🔐</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f0f4f8;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
    }
    .card {
      max-width: 600px;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    footer {
      position: fixed;
      bottom: 10px;
      width: 100%;
      text-align: center;
      font-size: 0.9em;
      color: gray;
    }
  </style>
</head>
<body>

  <div class="card text-center">
    <h2 class="mb-2"><strong>CyberShield_Her</strong> 🔐</h2>
    <p class="text-muted mb-4">AI-powered Job Scam Detection System for Women</p>

    <form method="POST">
      <div class="mb-3 text-start">
        <label class="form-label"><strong>Job URL (Optional)</strong></label>
        <input type="text" class="form-control" name="url" placeholder="Paste job posting URL (optional)">
      </div>
      <div class="mb-3 text-start">
        <label class="form-label"><strong>Job Title</strong></label>
        <input type="text" class="form-control" name="title" placeholder="e.g., Marketing Executive" required>
      </div>
      <div class="mb-3 text-start">
        <label class="form-label"><strong>Job Description</strong></label>
        <textarea class="form-control" name="description" rows="6" placeholder="Paste full job description..." required></textarea>
      </div>
      <button type="submit" class="btn btn-primary w-100">Check Job Post</button>
    </form>

    {% if result %}
      <div class="alert mt-4 {{ 'alert-danger' if 'Scam' in result else 'alert-success' }}">
        <strong>Prediction:</strong> {{ result }}
      </div>
      {% if url %}
        <div class="mt-2 text-start">
          <strong>Job URL:</strong> {{ url }}
        </div>
      {% endif %}
    {% endif %}
  </div>

  <footer>
    &copy; 2025 CyberShield_Her | Women-Centric Cybersecurity
  </footer>

</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def detect():
    result = ""
    job_url = ""
    if request.method == 'POST':
        # Get form data
        job_url = request.form['url']
        job_title = request.form['title']
        job_desc = request.form['description']
        combined_text = job_title + " " + job_desc

        # Predict
        input_vec = vectorizer.transform([combined_text])
        pred = model.predict(input_vec)[0]
        result = "⚠️ Scam Job Posting" if pred == 1 else "✅ Legitimate Job Posting"

        # Save to DB
        conn = sqlite3.connect("job_results.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO results (job_title, job_description, job_url, prediction, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            job_title,
            job_desc,
            job_url,
            result,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    return render_template_string(html, result=result, url=job_url)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
