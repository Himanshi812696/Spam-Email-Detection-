from flask import Flask, render_template, request, send_file
from io import BytesIO
import pickle
from joblib import load as joblib_load
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

app = Flask(__name__)

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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

@app.route("/favicon.ico")
def favicon():
    favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <rect width="100" height="100" fill="#667eea" rx="20"/>
        <text x="50" y="65" font-size="70" text-anchor="middle" fill="white">📧</text>
    </svg>'''
    return send_file(BytesIO(favicon_svg.encode()), mimetype="image/svg+xml")

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
    app.run(host="0.0.0.0", port=port, debug=True)