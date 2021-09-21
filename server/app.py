from flask import Flask, render_template, request, json

app = Flask(__name__)


student_data = {
    1: {"name": "슈퍼맨", "score": {"국어": 90, "수학": 65}},
    2: {"name": "배트맨", "score": {"국어": 75, "영어": 80, "수학": 75}}
}

@app.route("/test", methods=['POST']) #flask 웹 페이지 경로 
def post(): # 경로에서 실행될 기능 선언 
    print('ddd')

    data = request.get_json()
    print(data)
    #value = request.form['name']
    #print(value)
    return "hello world" 

@app.route("/backtest/<coin>")
def testing(coin):
   
    print(ohlcv)

    ohlcv2 = test1.upbit_backTesting2()
    print(ohlcv2)

    return render_template("backtest.html",
            template_ohlcv = ohlcv, 
            template_ohlcv2 = ohlcv2)

@app.route("/backtest/restAPI/<coin>", methods = ['GET'])
def getJson(coin):
    if(request.method == 'GET'):
        ohlcv = test1.upbit_backTesting(coin)



        print(jsonify(student_data)) 
        return jsonify(student_data)
    
@app.route('/user/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'

@app.route('/')
def index():
    return render_template("backtest.html",name = 'won')

@app.route("/student/<int:id>")
def student(id):
    return render_template("student.html", 
            template_name=student_data[id]["name"], 
            template_score=student_data[id]["score"])

if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=9000, debug=True) # host주소와 port number 선언


#http://hleecaster.com/flask-form/