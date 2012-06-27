function sparkline(dataset, container) {
    return new Highcharts.Chart({
        chart: {
            renderTo: container,
            defaultSeriesType: 'area',
            margin:[0,0,0,0]
        },
        title:{
            text:''
        },
        credits:{
            enabled:false
        },
        xAxis: {
            labels: {
                enabled:false
            }
        },
        yAxis: {
            maxPadding:0,
            minPadding:0,
            endOnTick:false,
            labels: {
                enabled:false
            }
        },
        legend: {
            enabled:false
        },
        tooltip: {
            enabled:false
        },
        plotOptions: {
            series:{
                lineWidth:1,
                shadow:false,
                states:{
                    hover:{
                        lineWidth:1
                    }
                },
                marker:{
                    enabled:false,
                    radius:1,
                    states:{
                        hover:{
                            radius:2
                        }
                    }
                }
            }
        },
        series: [{
            color:'#4A4A4A',
            fillColor:'rgba(150, 150, 150,.25)',
            data: dataset
        }]
    });
}