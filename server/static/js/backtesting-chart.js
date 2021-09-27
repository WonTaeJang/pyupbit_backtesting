var hpr_Chart;

function chartjs_setting(pyList){
    var arr = [];
    var arr_hpr = [];

    for (let i = 0; i < pyList["test"].length; i++) {
        arr.push(pyList["test"][i].datetime);
        arr_hpr.push(pyList["test"][i].hpr);
    }

    const data = {
        labels: arr,
        datasets: [{
            label: '변동성 돌파 전략 누적 수익률',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: arr_hpr,
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            borderColor: function(){
                return 'rgb(255, 255, 132)';
            }
            // borderColor: function(context, options) {
            //     var color = options.color; // resolve the value of another scriptable option: 'red', 'blue' or 'green'
            //     return Chart.helpers.color(color).lighten(0.2);
            // }
        }
    };


    // create canvas
    if(hpr_Chart!=null){
        hpr_Chart.destroy();
    }
    else{
        hpr_Chart = new Chart(
            document.getElementById('testChart'),
            config
        );
    }
    
}
