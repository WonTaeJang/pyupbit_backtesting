var hpr_Chart, mdd_Chart;

function chartjs_setting(pyList){
    var arr = [];
    var arr_hpr = [];
    var arr_mdd = [];

    for (let i = 0; i < pyList["test"].length; i++) {
        arr.push(pyList["test"][i].datetime);
        arr_hpr.push(pyList["test"][i].hpr);
        arr_mdd.push(pyList["test"][i].dd);
    }

    const hpr_data = {
        labels: arr,
        datasets: [{
            label: '변동성 돌파 전략 누적 수익률',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: arr_hpr,
        }]
    };

    const mdd_data = {
        labels: arr,
        datasets: [{
            label: '변동성 돌파 전략 MDD',
            backgroundColor: 'rgb(131, 220, 183)',
            borderColor: 'rgb(131, 220, 183)',
            data: arr_mdd,
        }]
    };

    const hpr_config = {
        type: 'line',
        data: hpr_data,
        options: {}
    };

    const mdd_config = {
        type: 'bar',
        data: mdd_data,
        options: {}
    };


    // create canvas
    if(hpr_Chart!=null){
        hpr_Chart.destroy();
    }

    if(mdd_Chart!=null){
        mdd_Chart.destroy();
    }
   
    hpr_Chart = new Chart(
        document.getElementById('hprChart'),
        hpr_config
    );

    mdd_Chart = new Chart(
        document.getElementById('mddChart'),
        mdd_config
    )
    
}
