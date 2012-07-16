function cf_sparkline(dataset, container) {
  return new Highcharts.Chart({
    chart: {
      renderTo: container,
      defaultSeriesType: 'area',
      margin:[0,0,0,0],
      backgroundColor: '#F3F3F3',
      borderWidth: 0
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
    subtitle: {
      text: 'Dados de todos os tempos'
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
      tickInterval: 5,
      title: {
        text: null
      },
      labels: {
        formatter: function() {
          return this.value + '%';
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

function cf_feelings_percentages_last_hours(categories, dataset, names, colors, title, container) {
  var new_series = [];
  for(var i=0; i<names.length; i++) {
    new_series.push({name: names[i], data: dataset[i], color: colors[i]});
  }
  return new Highcharts.Chart({
    chart: {
      renderTo: container,
      type: 'spline'
    },
    title: {
      text: title,
      x: -20 //center
    },
    credits:{
      enabled:false
    },
    xAxis: {
      categories: categories,
      enabled: true,
      // title: {
      //     text: 'Hora do dia'
      // },
      labels: {
        formatter: function() {
          return this.value + '-' + (parseInt(this.value, 10) + 1).toString() + 'h';
        },
        rotation: -45,
        align: 'right'
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: null
      },
      labels: {
        formatter: function() {
          return this.value + '%';
        }
      }
    },
    tooltip: {
      formatter: function() {
          return '<b>'+ this.series.name +'</b><br/>'+
            this.x + '-' + (this.x + 1) +'h: '+ Math.round(this.y*10)/10 +'%';
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

function cf_weather_conditions_for_feelings(categories, dataset, names, colors, title, container) {
  var new_series = [];
  for(var i=0; i<names.length; i++) {
    new_series.push({name: names[i], data: dataset[i], color: colors[i]});
  }
  dyn_rotation = categories.length > 10 ? -45 : 0;
  dyn_align = categories.length > 10 ? 'right' : 'center';
  return new Highcharts.Chart({
    chart: {
      renderTo: container,
      type: 'column'
    },
    credits:{
      enabled:false
    },
    title: {
      text: title
    },
    xAxis: {
      categories: categories,
      labels: {
        rotation: dyn_rotation,
        align: dyn_align
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: null
      },
      labels: {
        formatter: function() {
          return this.value + '%';
        }
      }
    },
    tooltip: {
      formatter: function() {
        return '<b>'+ this.series.name +'</b><br/>'+
          this.x +': ' + Math.round(this.percentage*10)/10 +'%';
      }
    },
    plotOptions: {
      column: {
        stacking: 'percent'
      }
    },
    series: new_series
  });
}

function cf_feelings_percentages_and_mean_last_hour(categories, dataset, names, feeling_color, container) {
  var new_series = [];
  for(var i=names.length-1; i>=0; i--) {
    new_series.push({name: names[i], data: dataset[i]});
  }
  new_series[1]['color'] = feeling_color;
  new_series[1]['legendIndex'] = 0;
  new_series[0]['color'] = '#BFBFBF';
  new_series[0]['legendIndex'] = 1;
  new_series[0]['dashStyle'] = 'ShortDash';
  return new Highcharts.Chart({
    chart: {
      renderTo: container,
      type: 'spline'
    },
    title: {
      text: capitaliseFirstLetter(names[0]) + ' nas últimas 24 horas',
      x: -20 //center
    },
    credits:{
      enabled:false
    },
    xAxis: {
      categories: categories,
      enabled: true,
      labels: {
        formatter: function() {
          return this.value + '-' + (parseInt(this.value, 10) + 1).toString() + 'h';
        },
        rotation: -45,
        align: 'right'
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: null
      },
      labels: {
        formatter: function() {
          return this.value + '%';
        }
      }
    },
    tooltip: {
      formatter: function() {
          return '<b>'+ this.series.name +'</b><br/>'+
            this.x + '-' + (this.x + 1) +'h: '+ Math.round(this.y*10)/10 +'%';
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

function cf_feelings_mean_percentages_every_two_hours(categories, dataset, title, container) {
  return new Highcharts.Chart({
    chart: {
        renderTo: container,
        polar: true
    },
    title: {
        text: title
    },
    credits:{
      enabled:false
    },
    pane: {
        center: ['50%', '50%'],
        size: '100%'
    },
    xAxis: {
        categories: categories,
        tickmarkPlacement: 'on',
        gridLineWidth: 0,
        // gridLineWidth: 2, // tradional radial graph
        lineWidth: 0,
        labels: {
            enabled: false
        }
    },
    yAxis: {
        gridLineWidth: 0,
        labels: {
            enabled: false
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        type: 'column',
        // type: 'area', // tradional radial graph
        data: dataset,
        lineWidth: 0,
        marker: {
            enabled: false
        },
        shadow: true
        // shadow: true // tradional radial graph
    }]
  });
}