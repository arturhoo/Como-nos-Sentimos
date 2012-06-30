function cf_sparkline(dataset, container) {
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

function cf_feelings_percentages_for_state(categories, dataset, state, container) {
    return new Highcharts.Chart({
        chart: {
            renderTo: container,
            type: 'column'
        },
        title: {
            text: 'Sentimentos de ' + state
        },
        credits:{
            enabled:false
        },
        xAxis: {
            categories: categories,
            enabled: false
        },
        yAxis: {
            min: 0,
            title: {
                text: null
            },
            labels: {
                formatter: function() {
                    return this.value + ' %';
                }
            }

        },
        legend: {
            enabled: false
        },
        tooltip: {
            formatter: function() {
                return this.x +': '+ Math.round(this.y*10)/10 +'%';
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
            series: [{
            data: dataset
        }]
    });
}

function cf_feelings_percentages_last_hours(categories, dataset, names, container) {
    var new_series = [];
    console.log(categories);
    console.log(names);
    console.log(dataset);
    for(var i=0; i<names.length; i++) {
        new_series.push({name: names[i], data: dataset[i]});
    }
    console.log(new_series);
    return new Highcharts.Chart({
        chart: {
            renderTo: container,
            type: 'spline'
        },
        title: {
            text: 'Sentimentos mais frequentes nas últimas 24 horas',
            x: -20 //center
        },
        credits:{
            enabled:false
        },
        xAxis: {
            categories: categories,
            enabled: true,
            text: 'Hora do dia'
        },
        yAxis: {
            min: 0,
            title: {
                text: null
            },
            labels: {
                formatter: function() {
                    return this.value + ' %';
                }
            }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +'h: '+ Math.round(this.y*10)/10 +'%';
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -10,
            y: 100,
            borderWidth: 0
        },
        series: new_series
    });
}
