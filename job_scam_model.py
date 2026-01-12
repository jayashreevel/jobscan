# job_scam_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("fake_job_postings.csv")

# Keep necessary columns and drop missing values
df = df[['title', 'description', 'fraudulent']].dropna()

# Balance dataset: equal number of scam (1) and legit (0)
legit = df[df['fraudulent'] == 0]
scam = df[df['fraudulent'] == 1]

# Downsample legitimate jobs to match number of scams
legit_sample = legit.sample(n=len(scam), random_state=42)
balanced_df = pd.concat([legit_sample, scam])

# Shuffle dataset
balanced_df = balanced_df.sample(frac=1, random_state=42)

# Combine title and description
balanced_df["text"] = balanced_df["title"] + " " + balanced_df["description"]

# Features and labels
X = balanced_df["text"]
y = balanced_df["fraudulent"]

# TF-IDF vectorizer with bigrams and max features
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, "job_scam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
