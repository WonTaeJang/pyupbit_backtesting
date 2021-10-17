from flask import Flask, render_template, request, json
import backtesting

app = Flask(__name__)

@app.route("/test", methods=['POST']) #flask 웹 페이지 경로 
def post(): # 경로에서 실행될 기능 선언 

    data = request.get_json()
    print(type(data))
    # value = request.form['name']
    # print(value)
    return "hello world" 

@app.route("/coin", methods=['POST']) #flask 웹 페이지 경로 
def post2(): # 경로에서 실행될 기능 선언 
    data = eval(request.get_json())
    #print(data)

    name = data['name']
    count = data['count']
    to = data['to']
    K = data['K']
    _interval = data['interval']

    json_val = backtesting.upbit_backTesting(name, count, to, K, _interval)

   
    print(json_val)
    return json_val

@app.route('/')
def index():
    kr_trickers = backtesting.get_tickers()

    return render_template("backtest.html",trickers = kr_trickers)

@app.route('/nondata')
def index2():
    return render_template("backtest.html")

if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=9001, debug=True) # host주소와 port number 선언


#http://hleecaster.com/flask-form/