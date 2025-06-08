from ml_utils import prepare_ml_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Coin listesi
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

def train_and_save_model(symbol):
    print(f"\n🔧 {symbol} için model eğitiliyor...")

    features, labels = prepare_ml_dataset(symbol)

    # CSV olarak kaydet
    os.makedirs("datasets", exist_ok=True)
    features.to_csv(f"datasets/{symbol}_features.csv", index=False)
    labels.to_csv(f"datasets/{symbol}_labels.csv", index=False)
    print(f"✅ {symbol} verileri CSV olarak kaydedildi.")
    

    # Modeli eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)

    preds = model.predict(features)
    print(f"\n📊 {symbol} için performans raporu:")
    print(classification_report(labels, preds))

    # Modeli kaydet
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, f"models/{symbol}_model.pkl")
    print(f"✅ Model kaydedildi: models/{symbol}_model.pkl")

if __name__ == "__main__":
    for symbol in symbols:
        train_and_save_model(symbol)
