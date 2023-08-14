import pandas as pd

def ema(data, period, smoothing):
  # Utwórz serię pandas z danymi
  data = pd.Series(data)
  # Oblicz współczynnik wygładzania jako 2 / (period + 1)
  smoothing = 2 / (period + 1)
  # Oblicz EMA jako średnią ważoną danych, gdzie wagi maleją wykładniczo
  ema = data.ewm(alpha=smoothing, adjust=False).mean()
  # Zwróć serię EMA
  return ema

# Zdefiniuj funkcję do obliczania TEMA dla danej serii danych i okresu
def tema(data, period):
  # Oblicz pierwszą EMA z danymi i okresem
  ema1 = ema(data, period, smoothing=None)
  # Oblicz drugą EMA z pierwszą EMA i okresem
  ema2 = ema(ema1, period, smoothing=None)
  # Oblicz trzecią EMA z drugą EMA i okresem
  ema3 = ema(ema2, period, smoothing=None)
  # Oblicz TEMA jako trzykrotność pierwszej EMA minus trzykrotność drugiej EMA plus trzecią EMA
  tema = 3 * ema1 - 3 * ema2 + ema3
  # Zwróć serię TEMA
  return tema