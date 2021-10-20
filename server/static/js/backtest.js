function settings(){
    var m = new Date();
    var pyupbit_result_list;
    var max_date = m.getFullYear() + '-' + (m.getMonth() + 1).toString().padStart(2, '0') + '-' + m.getDate().toString().padStart(2, '0');
    document.getElementById('date_start').min = '2021-06-01'
    document.getElementById('date_start').max = max_date
    document.getElementById('date_end').min = '2021-06-01'
    document.getElementById('date_end').max = max_date
    document.getElementById('date_end').value = max_date
    
    const request = new XMLHttpRequest();
    
    // 요청 초기화 
    document.getElementById('btn1').addEventListener("click", function () {
        request.open('POST', '/coin', true);
        request.setRequestHeader('Content-type', 'application/json');
    
        // name
        var coin_index = document.getElementById('select1').selectedIndex;
        var coin_name = document.getElementById('select1').options[coin_index].value;
    
        // interval
        var selected_index = document.getElementById('interval').selectedIndex;
        var interval = document.getElementById('interval').options[selected_index].value;

        // datetime
        
        var end = new Date(document.getElementById('date_end').value)
        var toEnd = end.getFullYear() + (end.getMonth() + 1) + end.getDate();
    
        // start는 day일때 날짜로 취급하고 그외는 count
        var start, elapsedMSec, elapsedDay;

        if(interval == 'day')
        {
            start = new Date(document.getElementById('date_start').value)
            elapsedMSec = end.getTime() - start.getTime();
            elapsedDay = ((elapsedMSec / 1000 / 60 / 60 / 24) + 1);
        }
        else
        {
            var coin_range_index = document.getElementById('coin_range').selectedIndex;
            var _range =  document.getElementById('coin_range').options[coin_range_index].value;
            elapsedDay = _range;
        }
    
        // K
        var K = document.getElementById('setValue_K').value;

    
        var pyupbit_json = "{'name':'" + coin_name + "', 'count':" + elapsedDay + ", 'to':'" + toEnd + "', 'K': " + K + ", 'interval': '" + interval +"'}"; // "KRW-BTC", 10, '20210301'
        console.log(pyupbit_json);
        request.send(JSON.stringify(pyupbit_json));
    
        // 4. onreadystatechage 이벤트리스너 등록 
        request.onreadystatechange = function (event) {
            // 1) 데이터를 다 받았고, 2) 응답코드 200(성공)을 받았는지 체크 
            if (request.readyState == 4 && request.status == 200) {
                // 응답받은 데이터 체크 

                pyupbit_result_list = JSON.parse(request.responseText);
                //const responseData = request.responseText;
                //document.getElementById('result_lb_1').innerText = pyupbit_result_list;

                result_label(pyupbit_result_list);

                chartjs_setting(pyupbit_result_list);
            }
        }
    });

    // interval의 case에 따라서 coin_range tag 변경됨
    document.getElementById('interval').addEventListener("change", function(){
        var selected_index = document.getElementById('interval').selectedIndex;
        var interval = document.getElementById('interval').options[selected_index].value;

        if(interval != "day"){
            document.getElementById('date_start').style.display = 'none';
            document.getElementById('coin_range').style.display = '';
        }
        else
        {
            document.getElementById('date_start').style.display = '';
            document.getElementById('coin_range').style.display = 'none';
        }
    });
}

function result_label(pyupbit_result_list){
    var investment =  document.getElementById('money').value != ''? document.getElementById('money').value.replace(/,/gi,'') : 0;    // 정규식으로 해야지 replaceAll이 된다.

    var count = pyupbit_result_list.test.length;
    var rate = (parseFloat(pyupbit_result_list.test[count-1].hpr) - 1) * 100;

    document.getElementById('result_div').style.visibility = "visible";

    // 테스팅 기간
    document.getElementById('result_lb_1').innerText = document.getElementById('date_start').value;
    document.getElementById('result_lb_6').innerText = document.getElementById('date_end').value;

    // 시작금액
    document.getElementById('result_lb_2').innerText = parseFloat(investment).toLocaleString();

    // MDD
    document.getElementById('result_lb_3').innerText = pyupbit_result_list.MDD;

    // 누적 수익률
    var income_hpr =  document.getElementById('result_lb_4');
    income_hpr.innerText = rate;

    // 손익평가
    var income_money = document.getElementById('result_lb_5');
    income_money.innerText = (parseFloat(investment)*parseFloat(pyupbit_result_list.test[count-1].hpr)).toLocaleString();

    if(income_hpr.innerText.toString().indexOf('-') == '-1')
    {
        // plus
        income_hpr.style.color = "red";
        income_money.style.color = "red";
    }
    else
    {
        // minus
        income_hpr.style.color = "blue";
        income_money.style.color = "blue";
    }

}

// 콤마 처리
function inputNumberFormat(obj) {
    obj.value = comma(uncomma(obj.value));
}

function comma(str) {
    str = String(str);
    return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}

function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}