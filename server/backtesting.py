import pyupbit
import numpy as np
import json

# upbit_backTesting("KRW-BTC", 10, '20210301')
def upbit_backTesting(coin, range, day, K):
    k = K

    # OHLCV (open, high, low, close, volume) 당일 시가, 고가, 저가, 종가, 거래량 
    df = pyupbit.get_ohlcv(coin, count = range, period=1, to=day)

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
    #print("MDD(%): ", df['dd'].max())
    print(df)
    #print(type(df))

    result = []
    result = df['open']

    # print(len(result))
    # print(df['open'][1])
    # print(result.index[0]) 

    return strToJson(df)

def strToJson(df):
    dict1 = {"test":[]}

    for i in range(len(df)):
        temp = {}
        
        for j in df:
            key = j
            value = str(df[j][i])
            temp[key] = value
        
        temp['datatime'] = df.index[i]
        dict1['test'].append(temp)

    #print(type(dict1))
    json_val = json.dumps(dict1, default=str)
    return json_val 


#json1 = upbit_backTesting("KRW-BTC", 200, '20210921',0.3)

def get_tickers():
    return pyupbit.get_tickers(fiat="KRW")
