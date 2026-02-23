from flask import Flask, render_template, request
import pickle
from joblib import load as joblib_load
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "spam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

try:
    model = joblib_load(model_path)
except Exception:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

try:
    model1 = joblib_load(vectorizer_path)
except Exception:
    with open(vectorizer_path, "rb") as e:
        model1 = pickle.load(e)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        message = request.form.get("message", "")
        features = model1.transform([message])
        prediction = model.predict(features)

        if prediction[0] == 1:
            result = "The message is likely to be SPAM"
        else:
            result = "The message is likely to be NOT SPAM"

        return render_template("index.html", prediction_text=result)
    except ValueError:
        return render_template("index.html", prediction_text="Invalid input. Enter a valid message.")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)