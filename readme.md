# AutoJudge – Programming Problem Difficulty Predictor

Name: Anurag Kishor Patil
Enrollment Number: 24114015
Branch: CSE

## Project Overview

AutoJudge is a machine learning–based system that automatically predicts the difficulty of competitive programming problems using only their textual descriptions and metadata. The project addresses the subjectivity and inconsistency of manual difficulty labeling across platforms such as Codeforces and Kattis.

The problem is formulated in two complementary ways:

* **Regression:** Predict a continuous difficulty score representing the relative hardness of a problem.
* **Classification:** Predict a discrete difficulty label (*easy*, *medium*, *hard*).

The final system integrates trained machine learning models with a **Flask-based web application** and a **Chrome browser extension** to provide real-time difficulty predictions.

---

## Datasets Used

Two publicly available datasets were used:

### 1. Kattis Problems Dataset

* Number of problems: ~4,100
* Provides both a numerical `problem_score` and explicit difficulty class labels.
* Used as the primary source for learning score–class relationships.

### 2. Codeforces Problems Dataset

* Number of problems: ~10,000
* Contains problem statements and ratings but **no explicit difficulty class labels**.
* Difficulty classes were derived using score thresholds inferred from the Kattis dataset.

Irrelevant metadata (contest IDs, tags, limits, etc.) was removed, and only textual and score-related fields were retained.
The link to datasets are provides in the report document

---

## Data Preprocessing

The following preprocessing steps were applied consistently during training and inference:

1. Dropping rows with missing ratings and filling remaining null text fields with empty strings.

2. Normalization of numerical scores (`rating` for Codeforces, `problem_score` for Kattis).

3. Derivation of difficulty classes for Codeforces using empirically observed Kattis score thresholds.

4. Conversion of sample input/output fields to string format.

5. Aggregation of all textual components into a single **combined text representation**:

   **Combined Text = Title + Description + Input + Output + Sample IO**

6. Text cleaning (whitespace normalization and standardization).

7. Merging both datasets into a single unified training dataframe.

---

## Feature Engineering

A hybrid feature representation was used, combining textual and numeric features.

### Textual Features

* **TF-IDF Vectorization** applied to the combined problem text.
* Captures important keywords and semantic structure.
* Results in a high-dimensional sparse feature matrix.

### Numeric Features

Four handcrafted numeric features were engineered:

1. **Constraint Magnitude:** Extracts large numerical constraints (e.g., 10^5, 10^9) and converts them to a logarithmic scale.
2. **Mathematical Density:** Counts mathematical symbols, operators, and LaTeX expressions.
3. **Algorithmic Keyword Count:** Counts occurrences of algorithm-related terms (dp, graph, dfs, binary search, etc.).
4. **Text Length:** Character length of the main problem description.

Textual and numeric features were concatenated to form the final input representation.

---

## Models and Approach

### Regression Models (Difficulty Score Prediction)

The following models were evaluated:

* Ridge Regression
* Random Forest Regressor
* **XGBoost Regressor**

**XGBoost Regressor** achieved the lowest MAE and highest R² score and was selected as the final regression model.

### Classification Models (Difficulty Class Prediction)

The following models were evaluated:

* Logistic Regression
* Linear SVM
* **XGBoost Classifier**

The **XGBoost Classifier** achieved the best accuracy and macro-averaged F1-score, indicating superior handling of non-linear feature interactions and class balance.

---

## Evaluation Metrics

### Regression Metrics

* Mean Absolute Error (MAE)
* R² Score

### Classification Metrics

* Accuracy
* Precision, Recall, F1-score (macro-averaged)
* Confusion Matrix

All experiments used an **80–20 train–test split** and a consistent preprocessing pipeline to avoid train–serve skew.

---

## Web Interface

A Flask-based web application was developed to demonstrate real-time predictions.

### Architecture

* Backend: Flask REST API
* Frontend: HTML + JavaScript
* Models loaded using `joblib`

### Functionality

* Users input problem details through a form.
* The backend extracts features and runs ML models.
* Outputs displayed:

  * Predicted difficulty class
  * Difficulty score (scaled for user interpretability)

---

## Browser Extension

A Chrome browser extension was developed to eliminate manual copy-pasting of problem statements.

### Architecture

* Content script for DOM extraction from problem webpages
* Popup UI built with HTML and JavaScript
* Backend communication via Flask REST API

### Functionality

* Automatically extracts problem text from Codeforces problem pages.
* Sends extracted content to the `/predict` API endpoint.
* Displays predicted difficulty class and score directly in the extension popup.

---

## Demo Video:
Link: https://youtu.be/lQb4QGTojd0

---

## Running the Project Locally

### 1. Backend Setup

```bash
python -m venv autojudge-env
autojudge-env\Scripts\activate
pip install \
numpy \
pandas \
scikit-learn \
xgboost \
scipy \
flask \
flask-cors \
joblib \
matplotlib \
seaborn
python app.py
```

The Flask server will start at `http://127.0.0.1:5000`.

### 2. Web Interface

* Open `http://127.0.0.1:5000` in a browser.
* Enter problem details and click **Predict Difficulty**.

### 3. Browser Extension

1. Open `chrome://extensions/`
2. Enable **Developer Mode**
3. Click **Load unpacked** and select the `Extension/` directory
4. Open a Codeforces problem page
5. Click the extension icon and press **Predict Difficulty**

### Note:
Change the file paths to your local directory path wherever required

---

## Conclusion

AutoJudge demonstrates that programming problem difficulty can be predicted reasonably well using a combination of textual analysis and machine learning. XGBoost models consistently outperform linear and tree-based baselines for both regression and classification tasks.

Future improvements may include transformer-based embeddings, incorporation of editorial or solution data, and cross-platform difficulty normalization.
