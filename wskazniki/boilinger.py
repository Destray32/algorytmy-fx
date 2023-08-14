import pandas as pd
import pandas_ta as ta

def BollingerBands(df, window, num_std):
    bands = df.ta.bbands(length=window, std=num_std)
    upper_band = bands[f'BBU_{window}_2.0']
    middle_band = bands[f'BBM_{window}_2.0']
    lower_band = bands[f'BBL_{window}_2.0']
    return pd.DataFrame({'Upper Band': upper_band, 'Middle Band': middle_band, 'Lower Band': lower_band})
