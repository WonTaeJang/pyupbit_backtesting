// datetime setting
var pyupbit_result_list;

function settings(){
    var m = new Date();
    var max_date = m.getFullYear() + '-' + (m.getMonth() + 1).toString().padStart(2, '0') + '-' + m.getDate().toString().padStart(2, '0');
    document.getElementById('date_start').min = '2021-06-01'
    document.getElementById('date_start').max = max_date
    document.getElementById('date_end').min = '2021-06-01'
    document.getElementById('date_end').max = max_date
    document.getElementById('date_end').value = max_date
    
    const request = new XMLHttpRequest();
    
    // 2. 요청 초기화 
    document.getElementById('btn1').addEventListener("click", function () {
        request.open('POST', '/coin', true);
        request.setRequestHeader('Content-type', 'application/json');
    
        // name
        var coin_index = document.getElementById('select1').selectedIndex;
        var coin_name = document.getElementById('select1').options[coin_index].value;
    
        // datetime
        var start = new Date(document.getElementById('date_start').value)
        var end = new Date(document.getElementById('date_end').value)
    
        var elapsedMSec = end.getTime() - start.getTime();
        var elapsedDay = ((elapsedMSec / 1000 / 60 / 60 / 24) + 1);
    
        var toEnd = end.getFullYear() + (end.getMonth() + 1) + end.getDate();
    
        // K
        var K = document.getElementById('setValue_K').value;
    
        var pyupbit_json = "{'name':'" + coin_name + "', 'count':" + elapsedDay + ", 'to':'" + toEnd + "', 'K': " + K + "}"; // "KRW-BTC", 10, '20210301'
        console.log(pyupbit_json);
        request.send(JSON.stringify(pyupbit_json));
    
        // 4. onreadystatechage 이벤트리스너 등록 
    
        request.onreadystatechange = function (event) {
            // 1) 데이터를 다 받았고, 2) 응답코드 200(성공)을 받았는지 체크 
            if (request.readyState == 4 && request.status == 200) {
                // 응답받은 데이터 체크 

                pyupbit_result_list = request.responseText;
                //const responseData = request.responseText;
                //document.getElementById('result_lb_1').innerText = responseData;
                console.log(pyupbit_result_list);
            }
        }
    });
}