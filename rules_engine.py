def evaluate_rules(rsi, macd, macd_signal, risk, term):
    if rsi is None or macd is None or macd_signal is None:
        return "Veri yetersiz."

    result = []
    if rsi < 30 and macd > macd_signal:
        result.append("Alım sinyali yüksek, yatırım yapılabilir.")
    if rsi > 70 and macd < macd_signal:
        result.append("Aşırı alım bölgesi, satış düşünülebilir.")
    if risk == "düşük" and rsi > 50 and macd < macd_signal:
        result.append("Bekle – piyasayı izlemeye devam et.")
    if risk == "yüksek" and term == "kısa":
        result.append("Kısa vadeli ve riskli fırsatlar değerlendirilebilir.")
    
    return result if result else ["Net bir sinyal yok, izlemeye devam."]
