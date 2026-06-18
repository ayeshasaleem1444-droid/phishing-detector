# train_corrected_final.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import sys
import time

sys.path.append('backend')
from backend.features import extract_features

print("=" * 70)
print("CORRECTED TRAINING - USING STANDARD DATASET LABELS (0=SAFE, 1=PHISHING)")
print("=" * 70)

start_time = time.time()

# Load dataset
df = pd.read_csv('data/dataset.csv')
print(f"\n📂 Loaded {len(df):,} total URLs")
print(f"   SAFE (0) count: {(df['label'] == 0).sum():,}")
print(f"   PHISHING (1) count: {(df['label'] == 1).sum():,}")

# Use 50,000 URLs for faster training
if len(df) > 50000:
    print(f"\n📊 Using 50,000 random URLs for faster training")
    df = df.sample(n=50000, random_state=42)
    print(f"   SAFE: {(df['label'] == 0).sum():,}")
    print(f"   PHISHING: {(df['label'] == 1).sum():,}")

# Extract features
print("\n🔍 Extracting features from URLs...")
print("   (This takes 2-4 minutes)")

X = []
urls = df['url'].tolist()
for i, url in enumerate(urls):
    if i % 10000 == 0 and i > 0:
        print(f"   Processed {i:,}/{len(urls):,} URLs")
    X.append(extract_features(url))

X = np.array(X)
y = df['label'].values  # Using original standard labels!

print(f"\n   Feature matrix: {X.shape}")
print(f"   Features per URL: {X.shape[1]}")

# Split data
print("\n📊 Splitting data into training (80%) and testing (20%)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("\n🤖 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Test model
print("\n📈 Testing model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'=' * 70}")
print(f"🎯 MODEL ACCURACY: {accuracy*100:.2f}%")
print(f"{'=' * 70}")

# Save model
print("\n💾 Saving model...")
joblib.dump(model, 'models/phishing_model.pkl')
print("   ✅ Model saved to: models/phishing_model.pkl")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['SAFE', 'PHISHING']))

elapsed_time = time.time() - start_time
print(f"\n⏱️ Total training time: {elapsed_time/60:.2f} minutes")
print("\n✅ TRAINING COMPLETE!")