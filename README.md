# 🤖 Kripto Para Uzman Sistemi

Bu proje, kripto para alım-satım önerileri veren gelişmiş bir uzman sistemdir. Makine öğrenmesi, teknik analiz ve kural motoru kullanarak BTC, ETH ve BNB için alım-satım sinyalleri üretir.

## 📋 İçindekiler

- [Proje Özeti](#proje-özeti)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Model Eğitimi](#model-eğitimi)
- [Backtest Sistemi](#backtest-sistemi)
- [Teknik Detaylar](#teknik-detaylar)
- [Sonuçlar](#sonuçlar)

## 🎯 Proje Özeti

Bu uzman sistem, Binance API'den gerçek zamanlı veri çekerek, teknik göstergeler hesaplar ve makine öğrenmesi modelleri ile alım-satım önerileri üretir. Sistem hem kural tabanlı hem de ML tabanlı yaklaşımları birleştirir.

### Neden Bu Proje?

- **Eğitim Amaçlı**: Uzman sistemler dersi için pratik uygulama
- **Gerçek Veri**: Binance API ile canlı kripto para verileri
- **Çoklu Yaklaşım**: Hem kural motoru hem makine öğrenmesi
- **Görselleştirme**: Anlaşılır grafikler ve performans analizi

## ✨ Özellikler

### 🔧 Teknik Analiz
- **25+ Teknik Gösterge**: RSI, MACD, Bollinger Bands, Stochastic, ADX, vb.
- **Feature Engineering**: Fiyat değişimleri, volatilite, hacim analizi
- **Zaman Özellikleri**: Saat, gün, hafta sonu etkileri

### 🤖 Makine Öğrenmesi
- **Random Forest**: Ana tahmin modeli
- **Hızlı Eğitim**: 300 veri, 8 temel gösterge ile optimize edilmiş
- **Overfitting Önleme**: Sıkı parametreler ve cross-validation

### 📊 Backtest Sistemi
- **100$ Başlangıç**: Gerçekçi test senaryosu
- **30 Günlük Test**: Son 30 günün verisi ile test
- **Performans Grafikleri**: Portföy değeri, işlem geçmişi, kar/zarar

### 🌐 Web Arayüzü
- **Flask Tabanlı**: Kullanıcı dostu web arayüzü
- **Gerçek Zamanlı**: Canlı fiyat ve sinyal gösterimi
- **Grafikler**: Plotly ile interaktif grafikler

## 🚀 Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### API Anahtarı
Binance API anahtarınızı `config.py` dosyasına ekleyin:
```python
BINANCE_API_KEY = "your_api_key"
BINANCE_SECRET_KEY = "your_secret_key"
```

## 📖 Kullanım

### 1. Model Eğitimi
```bash
python train_model.py
```
**Ne Yapar?**
- 300 saatlik veri çeker (yaklaşık 12 gün)
- 8 temel gösterge hesaplar: RSI, MACD, Stochastic, BB, SMA, ATR
- RandomForest modelini hızlı parametrelerle eğitir (20 ağaç, max_depth=3)
- Model, scaler ve özellik listesini kaydeder

**Neden Bu Parametreler?**
- **300 veri**: Hızlı eğitim için yeterli, overfitting riski düşük
- **8 gösterge**: Temel ve etkili göstergeler, karmaşıklık az
- **RandomForest**: Hızlı, güvenilir, feature importance sağlar

### 2. Backtest Çalıştırma
```bash
python backtest.py
```
**Ne Yapar?**
- 100$ başlangıç sermayesi ile test
- 30 günlük veri ile gerçekçi simülasyon
- Tüm pozisyonları kullanma stratejisi (all-in/all-out)
- 4 farklı grafik: portföy performansı, fiyat+işlemler, kar/zarar, özet

**Neden Bu Strateji?**
- **100$**: Küçük yatırımcı senaryosu
- **All-in**: Basit ve anlaşılır strateji
- **30 gün**: Yeterli test süresi, güncel veri

### 3. Web Arayüzü
```bash
python app.py
```
Tarayıcıda `http://localhost:5000` adresine gidin.

## 🔬 Model Eğitimi Detayları

### Veri Hazırlama
```python
# 1. Veri Çekme
df = get_klines(symbol, interval='1h', limit=300)

# 2. Teknik Göstergeler
df['RSI'] = ta.rsi(close, length=14)
df['MACD'] = ta.macd(close)['MACD_12_26_9']
df['Stoch_K'] = ta.stoch(high, low, close)['STOCHk_14_3_3']
# ... diğer göstergeler

# 3. Feature Engineering
df['price_change_1h'] = df['close'].pct_change(1)
df['SMA_cross'] = (df['SMA_20'] > df['SMA_50']).astype(int)
df['hour'] = df.index.hour
```

### Etiketleme Stratejisi
```python
# Gelecek 1 saatte %0.5'den fazla artış = AL (1)
# Gelecek 1 saatte %0.5'den fazla düşüş = SAT (-1)
# Diğer durumlar = BEKLE (0)
```

### Model Parametreleri
```python
RandomForestClassifier(
    n_estimators=20,    # Hızlı eğitim
    max_depth=3,        # Overfitting önleme
    random_state=42     # Tekrarlanabilirlik
)
```

## 📈 Backtest Sistemi Detayları

### İşlem Stratejisi
1. **AL Sinyali**: Tüm sermayeyi kullan, pozisyon al
2. **SAT Sinyali**: Tüm pozisyonu sat, kar/zarar hesapla
3. **BEKLE**: Hiçbir şey yapma

### Performans Metrikleri
- **Toplam Getiri**: Başlangıç → Bitiş yüzdesi
- **İşlem Sayısı**: Toplam AL/SAT işlemi
- **Kazanma Oranı**: Karlı işlemlerin yüzdesi
- **Portföy Değeri**: Zaman içindeki değişim

### Grafikler
1. **Portföy Performansı**: 100$ → Final değer
2. **Fiyat ve İşlemler**: Fiyat + AL/SAT noktaları
3. **Kar/Zarar**: Her işlemin sonucu
4. **Özet İstatistikler**: Tüm metrikler

## 🔧 Teknik Detaylar

### Kullanılan Kütüphaneler
- **pandas**: Veri işleme
- **numpy**: Matematiksel işlemler
- **scikit-learn**: Makine öğrenmesi
- **ta**: Teknik analiz göstergeleri
- **matplotlib/seaborn**: Grafikler
- **flask**: Web arayüzü
- **plotly**: İnteraktif grafikler

### Dosya Yapısı
```
crypto_expert_system/
├── app.py                 # Flask web uygulaması
├── train_model.py         # Model eğitimi
├── backtest.py           # Backtest sistemi
├── ml_utils.py           # ML yardımcı fonksiyonlar
├── config.py             # API anahtarları
├── models/               # Eğitilmiş modeller
├── datasets/             # Veri setleri
├── backtest_results/     # Backtest grafikleri
└── model_performance/    # Model performans grafikleri
```

### API Entegrasyonu
- **Binance API**: Gerçek zamanlı veri
- **Rate Limiting**: API limitlerine uyum
- **Error Handling**: Bağlantı hatalarını yönetme

## 📊 Sonuçlar

### Model Performansı
- **Eğitim Süresi**: ~30 saniye (hızlı parametreler)
- **Veri Boyutu**: 300 örnek, 8 özellik
- **Doğruluk**: %60-80 arası (gerçekçi beklenti)

### Backtest Sonuçları
- **Test Süresi**: 30 gün
- **Başlangıç**: $100
- **Grafikler**: 4 farklı analiz grafiği
- **Metrikler**: Getiri, işlem sayısı, kazanma oranı

### Web Arayüzü
- **Gerçek Zamanlı**: Canlı fiyat güncellemeleri
- **İnteraktif**: Plotly grafikleri
- **Kullanıcı Dostu**: Basit ve anlaşılır

## 🎓 Eğitim Amaçlı Kullanım

1. **Uzman Sistemler**: Kural motoru ve ML entegrasyonu
2. **Makine Öğrenmesi**: Veri hazırlama, model eğitimi, değerlendirme
3. **Teknik Analiz**: Finansal göstergeler ve hesaplamalar
4. **API Entegrasyonu**: Gerçek veri çekme ve işleme
5. **Backtesting**: Strateji test etme ve performans analizi
6. **Web Geliştirme**: Flask ile web uygulaması

## ⚠️ Önemli Notlar

- Bu proje **eğitim amaçlıdır**, gerçek yatırım tavsiyesi değildir
- Kripto para piyasaları yüksek risk içerir
- Model performansı geçmiş verilere dayanır, gelecek garantisi vermez
- API anahtarlarınızı güvenli tutun

## 🔄 Geliştirme Önerileri

1. **Daha Fazla Gösterge**: Williams %R, Ichimoku, vb.
2. **Farklı Modeller**: LSTM, XGBoost, Ensemble
3. **Risk Yönetimi**: Stop-loss, position sizing
4. **Gerçek Zamanlı Trading**: Otomatik işlem yapma
5. **Portföy Optimizasyonu**: Çoklu varlık yönetimi

---




