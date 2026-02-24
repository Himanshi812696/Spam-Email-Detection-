from flask import Flask, render_template, request
import pickle
from joblib import load as joblib_load
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "spam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

try:
    model = joblib_load(model_path)
except:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

try:
    vectorizer = joblib_load(vectorizer_path)
except:
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        message = request.form.get("message", "")

        if message.strip() == "":
            return render_template("index.html", prediction_text="Please enter a message.")

        features = vectorizer.transform([message])
        prediction = model.predict(features)

        result = "The message is likely to be SPAM 🚨" if prediction[0] == 1 else "The message is NOT SPAM ✅"

        return render_template("index.html", prediction_text=result)

    except Exception as e:
        print("Error:", e)
        return render_template("index.html", prediction_text="Error in prediction.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)