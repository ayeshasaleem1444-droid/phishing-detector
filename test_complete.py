# test_complete.py
import joblib
import sys

sys.path.append('backend')
from backend.features import extract_features

print("=" * 60)
print("COMPLETE MODEL TEST")
print("=" * 60)

# Load model
print("\n1. Loading model...")
model = joblib.load('models/phishing_model.pkl')
print("   ✅ Model loaded!\n")
# Test URLs (Updated to diagnose the shortcuts)
test_urls = [
    "https://www.google.com",                  # Triggers HTTPS & Brand trap
    "https://www.gooogle.com",                  
    "http://www.google.com",                   # Triggers Brand trap only
    "https://www.thissitehasnobrandname.com",  # Triggers HTTPS trap only
    "http://www.thissitehasnobrandname.com",   # Safe structure, no traps
    "http://paypal.com.verify-account.xyz",    # Real phishing structure
    "http://185.142.53.45/login",              # Real phishing structure
    "https://paypal.com.login.update.security.danger-site.com",
]


print("2. Testing URLs:\n")

for url in test_urls:
    features = extract_features(url)
    pred = model.predict([features])[0]
    prob = model.predict_proba([features])[0]
    
    print(f"URL: {url}")
    print(f"   Prediction: {pred} (0=SAFE, 1=PHISHING)")
    print(f"   SAFE: {prob[0]*100:.1f}% | PHISHING: {prob[1]*100:.1f}%")
    
    if pred == 0:
        print(f"   ➡️  Model says: SAFE\n")
    else:
        print(f"   ➡️  Model says: PHISHING\n")

print("=" * 60)

# Show model info
print("\n3. Model Info:")
print(f"   File size: {model.n_estimators} trees")
print(f"   Features per URL: {model.n_features_in_}")
print("=" * 60)