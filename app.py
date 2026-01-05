from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import joblib
import numpy as np
from scipy.sparse import hstack, csr_matrix
import re
import math
import unicodedata

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def find_constraints(inp):
    if not isinstance(inp, str):
        return 0.0

    text = unicodedata.normalize("NFKD", inp)
    text = re.sub(r"\\,\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)

    maxi = 0
    for b, e in re.findall(r"(\d+)\s*[⋅×*]\s*10\^\{(\d+)\}", text):
        maxi = max(maxi, int(b) * (10 ** int(e)))

    for b, e in re.findall(r"(\d+)\s*[⋅×*]\s*10\^(\d+)", text):
        maxi = max(maxi, int(b) * (10 ** int(e)))

    for e in re.findall(r"10\^\{(\d+)\}", text):
        maxi = max(maxi, 10 ** int(e))

    for e in re.findall(r"10\^(\d+)", text):
        maxi = max(maxi, 10 ** int(e))

    for b in re.findall(r"\b\d{1,}\b", text):
        maxi = max(maxi, int(b))

    return min(math.log10(maxi), 20) if maxi > 0 else 0.0


def find_math(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0.0

    m1 = text.count('$')
    m2 = len(re.findall(r"\\[a-zA-Z]+", text))
    m3 = len(re.findall(r"[=<>+\-*/^_]", text))
    
    return m1+m2+m3

ALGO_KEYWORDS = [
    "dp", "dynamic programming", "graph", "tree", "dfs", "bfs",
    "shortest path", "dijkstra", "flow",
    "segment tree", "fenwick", "bit", "bits"
    "binary search", "two pointers", "sliding window",
    "greedy", "divide and conquer", "topological sort", 
    "mod", "modulo", "prime", "gcd", "lcm",
    "combinatorics", "permutation", "combination",
    "probability", "expected value",
    "matrix", "geometry", "logarithm"
]

def find_algowords(text, keywords):
    text = text.lower()
    return sum(1 for kw in keywords if kw in text)




tfidf = joblib.load(r"C:\Users\asus\Desktop\ACM\models\tfidf.joblib")
scaler = joblib.load(r"C:\Users\asus\Desktop\ACM\models\scaler.joblib")
xgb_clf = joblib.load(r"C:\Users\asus\Desktop\ACM\models\xgb_clf.joblib")
xgb_reg = joblib.load(r"C:\Users\asus\Desktop\ACM\models\score_xgb.joblib")

CLASS_MAP = {0: "easy", 1: "medium", 2: "hard"}

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    title = data.get("title", "")
    description = data.get("description", "")
    input_description = data.get("input_description", "")
    output_description = data.get("output_description", "")
    sample_io = data.get("sample_io", "")

    combined_text = (
        "Title: " + clean_text(title) +
        " Description: " + clean_text(description) +
        " Input: " + clean_text(input_description) +
        " Output: " + clean_text(output_description) +
        " SampleIO: " + clean_text(sample_io)
    )

    text_length = len(description)

    numeric_features = np.array([[find_constraints(input_description), find_math(combined_text), find_algowords(combined_text, ALGO_KEYWORDS), text_length]])

    X_text = tfidf.transform([combined_text])        
    X_num = scaler.transform(numeric_features)      
    X_final = hstack([X_text, csr_matrix(X_num)])   

    pred_class_id = int(xgb_clf.predict(X_final)[0])
    pred_probs = xgb_clf.predict_proba(X_final)[0]

    score = float(xgb_reg.predict(X_final)[0])

    return jsonify({
        "predicted_class": CLASS_MAP[pred_class_id],
        "predicted_score": score,
        "class_probabilities": {
            "easy": float(pred_probs[0]),
            "medium": float(pred_probs[1]),
            "hard": float(pred_probs[2])
        }
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
