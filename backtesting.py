import pyupbit
import numpy as np

k = 0.3

# OHLCV (open, high, low, close, volume) 당일 시가, 고가, 저가, 종가, 거래량 
df = pyupbit.get_ohlcv("KRW-BTC", count = 5, period=1, to='20210301')

# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * k

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005
# ror(수익율), np.where(조건문)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 *100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD 계산, 고통 지수
print("MDD(%): ", df['dd'].max())
print(df)
#print(type(df))

result = []
result = df['open']

print(len(result))
print(df['open'][1])
print(result.index[0]) 
#df.to_excel("dd.xlsx1")