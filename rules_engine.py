import pandas as pd

def evaluate_rules(rsi, macd, macd_signal, risk, term):
    if pd.isna(rsi) or pd.isna(macd) or pd.isna(macd_signal):
        return ["Veri yetersiz."]
    
    result = []

    if rsi < 40 and macd > macd_signal:
        result.append("RSI < 40 ve MACD yükseliyor → Alım sinyali olabilir.")

    if rsi > 65 and macd < macd_signal:
        result.append("RSI > 65 ve MACD düşüyor → Satış sinyali olabilir.")

    if risk == "düşük" and rsi > 50 and macd < macd_signal:
        result.append("Düşük risk profili için sinyal zayıf, beklemeye geç.")
    
    if risk == "yüksek" and term == "kısa":
        result.append("Kısa vadeli fırsatlar değerlendirilebilir.")

    if not result:
        result.append("Net bir sinyal yok, izlemeye devam.")

    return result

