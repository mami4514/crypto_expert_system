from ml_utils import prepare_ml_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Veriyi hazırla
features, labels = prepare_ml_dataset("BTCUSDT")

# 2. Modeli eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

# 3. Performans raporu (isteğe bağlı)
preds = model.predict(features)
print(classification_report(labels, preds))

# 4. Modeli kaydet
joblib.dump(model, "ml_model.pkl")
print(" Model başarıyla ml_model.pkl dosyasına kaydedildi.")
