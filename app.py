from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sys

sys.path.append('backend')
from backend.features import extract_features, get_feature_names

app = Flask(__name__)
CORS(app)

# --- FIX 1: Prevent the app from running without a model ---
try:
    model = joblib.load('models/phishing_model.pkl')
    print("✅ AI Model successfully loaded into the API server!")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Could not load model: {e}")
    print("Stopping server initialization.")
    sys.exit(1) # Gracefully crash the server immediately

@app.route('/predict', methods=['POST'])
def predict_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    incoming_url = data['url']
    
    # ─── LIVE RUN DIAGNOSTICS ───
    print("\n" + "="*50)
    print(f"🔍 EVALUATING TARGET: {incoming_url}")
    
    features = extract_features(incoming_url)
    feature_names = get_feature_names()
    
    # Print calculated data vector
    print(f"📊 Vector Data: {features}")
    
    # 1. Catch Hybrid Rule
    try:
        typo_index = feature_names.index('is_typo')
        if features[typo_index] == 1:
            print("🚨 VERDICT: Caught by Hardcoded Typosquatting Rule")
            return jsonify({
                'url': incoming_url,
                'prediction': 1,
                'status': 'PHISHING',
                'confidence': 100.0,
                'reason': 'Brand Look-Alike Domain Detected (Strict Rule)'
            })
    except ValueError:
        print("⚠️ Warning: 'is_typo' not found in feature names list!")
    
    # 2. Catch ML Prediction
    # NOTE: Ensure 'features' is a list ordered identically to your training dataset layout
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    
    safe_score = float(probabilities[0] * 100)
    phish_score = float(probabilities[1] * 100)
    
    print(f"🤖 AI Assessment -> Safe: {safe_score:.2f}% | Phish: {phish_score:.2f}%")
    
    if prediction == 1:
        print("🚨 VERDICT: Caught by Machine Learning Tree Rules")
        return jsonify({
            'url': incoming_url,
            'prediction': 1,
            'status': 'PHISHING',
            'confidence': round(phish_score, 2),
            'reason': 'Structural layout matches phishing patterns (AI)'
        })
    else:
        print("🟢 VERDICT: Safe Domain Allowed")
        return jsonify({
            'url': incoming_url,
            'prediction': 0,
            'status': 'SAFE',
            'confidence': round(safe_score, 2),
            'reason': 'URL structure looks clean (AI)'
        })

if __name__ == '__main__':
    app.run(port=5000, debug=True)