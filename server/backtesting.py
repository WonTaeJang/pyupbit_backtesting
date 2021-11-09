import pyupbit
import numpy as np
import json
import time

# upbit_backTesting("KRW-BTC", 10, '20210301','0.32')


# coin: 종목
# range: 조회 개수
# day: 조회 끝나는 일
# _interval: 조회 단위 ('day', 'minute' ,'week')
 
# 변동성 돌파전략
# 오늘 시가: 09:00, 오늘 종가: 08:59
# 변동폭(어제 고가 - 어제 저가) * K + 오늘 시가 를 매수 타이밍으로 보고 다음날 08:59(종가)에 매도하는 전략

def upbit_backTesting(coin, range, day, K, _interval):
    k = K
    
    # OHLCV (open, high, low, close, volume) 당일 시가, 고가, 저가, 종가, 거래량 
    df = pyupbit.get_ohlcv(coin, count = range, period=1, to=day, interval=_interval)

    # 변동폭 * k 계산, (고가 - 저가) * k값
    
    df['range'] = (df['high'] - df['low']) * k

    # target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
    # 어제의 고가 - 저가 (변동폭) * K 한 값 = 매수가 // 매수가 이상이면 매수를 진행한다.
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
    #print(df)
    #print(type(df))

    result = []
    result = df['open']

    # print(len(result))
    # print(df['open'][1])
    # print(result.index[0]) 

    return strToJson(df)

def strToJson(df):
    dict1 = {"test":[], "MDD":""}

    for i in range(len(df)):
        temp = {}
        
        for j in df:
            key = j
            value = str(df[j][i])
            temp[key] = value
        
        strr = df.index[i]
        temp['datetime'] = str(strr)[5:-3]
        
        dict1['test'].append(temp)

    dict1['MDD'] = df['dd'].max()

    #print(type(dict1))
    json_val = json.dumps(dict1, default=str)
    return json_val 


#json1 = upbit_backTesting("KRW-BTC", 10, '20210301',0.3,'day')

def get_tickers():
    return pyupbit.get_tickers(fiat="KRW")


# 가장 좋은 k값 구하기
def get_best_k(coin, range, day, _interval):
    best_ror = 0
    best_k = 0

    # 소수점 첫번째 자리 K 값 구하기
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(coin, range, day, k, _interval)
        #print("%.1f %f" % (k, ror))

        if best_ror < ror:
            best_ror = ror
            best_k = k

    print(best_k, best_ror)    

    time.sleep(5)

    for k in np.arange(best_k, (best_k + 0.09), 0.01):
        temp_k = round(k,3)
        ror2 = get_ror(coin, range, day, temp_k, _interval)

        if best_ror < ror2:
            best_ror = ror2
            best_k = temp_k
    
    print(best_k, best_ror) 
#        print("%.1f %f" % (k, ror))

def get_ror(coin, range, day, k, _interval):
    df = pyupbit.get_ohlcv(coin, count = range, period=1, to=day, interval=_interval)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
 
    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                        df['close'] / df['target'] - fee,
                        1)
 
    #print(df)

    ror = df['ror'].cumprod()[-2]
    return ror

json1 = get_best_k("KRW-BTC", 100, '20211108','day')