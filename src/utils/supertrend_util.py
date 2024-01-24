import numpy as np
import pandas as pd

class SupertrendUtil:

    @classmethod
    def get_indicators(self, high, low, close, lookback, multiplier):
    
        # ATR
        
        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
        atr = tr.ewm(lookback).mean()
        
        # H/L AVG AND BASIC UPPER & LOWER BAND
        
        hl_avg = (high + low) / 2
        upper_band = (hl_avg + multiplier * atr).dropna()
        lower_band = (hl_avg - multiplier * atr).dropna()
        
        # FINAL UPPER BAND
        
        final_bands = pd.DataFrame(columns = ['upper', 'lower'])
        final_bands.iloc[:,0] = [x for x in upper_band - upper_band]
        final_bands.iloc[:,1] = final_bands.iloc[:,0]
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i,0] = 0
            else:
                if (upper_band.iloc[i] < final_bands.iloc[i-1,0]) | (close.iloc[i-1] > final_bands.iloc[i-1,0]):
                    final_bands.iloc[i] = upper_band.iloc[i]
                else:
                    final_bands.iloc[i,0] = final_bands.iloc[i-1,0]
        
        # FINAL LOWER BAND
        
        for i in range(len(final_bands)):
            if i == 0:
                final_bands.iloc[i, 1] = 0
            else:
                if (lower_band.iloc[i] > final_bands.iloc[i-1,1]) | (close.iloc[i-1] < final_bands.iloc[i-1,1]):
                    final_bands.iloc[i,1] = lower_band.iloc[i]
                else:
                    final_bands.iloc[i,1] = final_bands.iloc[i-1,1]
        
        # SUPERTREND
        
        supertrend = pd.DataFrame(columns = [f'supertrend_{lookback}'])
        supertrend.iloc[:,0] = [x for x in final_bands['upper'] - final_bands['upper']]
        
        for i in range(len(supertrend)):
            if i == 0:
                supertrend.iloc[i, 0] = 0
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close.iloc[i] < final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 0] and close.iloc[i] > final_bands.iloc[i, 0]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close.iloc[i] > final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 1]
            elif supertrend.iloc[i-1, 0] == final_bands.iloc[i-1, 1] and close.iloc[i] < final_bands.iloc[i, 1]:
                supertrend.iloc[i, 0] = final_bands.iloc[i, 0]
        
        supertrend = supertrend.set_index(upper_band.index)
        supertrend = supertrend.dropna()[1:]
        
        # ST UPTREND/DOWNTREND
        
        upt = []
        dt = []
        close = close.iloc[len(close) - len(supertrend):]

        for i in range(len(supertrend)):
            if close.iloc[i] > supertrend.iloc[i, 0]:
                upt.append(supertrend.iloc[i, 0])
                dt.append(np.nan)
            elif close.iloc[i] < supertrend.iloc[i, 0]:
                upt.append(np.nan)
                dt.append(supertrend.iloc[i, 0])
            else:
                upt.append(np.nan)
                dt.append(np.nan)
                
        st, upt, dt = pd.Series(supertrend.iloc[:, 0]), pd.Series(upt), pd.Series(dt)
        upt.index, dt.index = supertrend.index, supertrend.index
        
        return st, upt, dt
    

    def get_signals(self, prices, st):
        buy_price = []
        sell_price = []
        st_signal = []
        signal = 0
        
        for i in range(len(st)):
            if st.iloc[i-1] > prices.iloc[i-1] and st.iloc[i] < prices.iloc[i]:
                if signal != 1:
                    buy_price.append(prices.iloc[i])
                    sell_price.append(np.nan)
                    signal = 1
                    st_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    st_signal.append(0)
            elif st.iloc[i-1] < prices.iloc[i-1] and st.iloc[i] > prices.iloc[i]:
                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(prices.iloc[i])
                    signal = -1
                    st_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    st_signal.append(0)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                st_signal.append(0)
                
        return buy_price, sell_price, st_signal

