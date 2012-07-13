function theme_highchart() {
    Highcharts.theme = {
      chart: {
        backgroundColor: '#F9F9F9',
        style: {
         fontFamily: 'Helvetica',
         paddingBottom: '20px'
        }
      },
      title: {
        style: {
         color: '#505050',
         fontSize: '14px'
        }
      },
      subtitle: {
        style: {
         color: '#505050'
        }
      },
      xAxis: {
        title: {
          style: {
            color: '#737373'
          }
        }
      },
      legend: {
        itemStyle: {
          color: '#737373'
        }
      }
    };
    var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
}


function do_feelings_percentages_last_hour(feelings_percentages_last_hours) {
    var dataset = [];
    var names = [];
    var categories = [];
    for(var i=0; i<feelings_percentages_last_hours.length; i++) {
      entry = feelings_percentages_last_hours[i];
      if(i === 0) {
        for(var j=0; j<entry[1].length; j++) {
          var hours = entry[1][j];
          categories.push(hours[0]);
        }
      }
      names.push(entry[0]);
      data_entry = [];
      for(var k=0; k<entry[1].length; k++) {
        data = entry[1][k];
        data_entry.push(data[1]);
      }
      dataset.push(data_entry);
    }
    if(feelings_percentages_last_hours.length !== 0) {
      $('<div/>', {
        id: 'feelings_chart',
        class: 'charts-border'
      }).appendTo('#stats');
      $('<div/>', {
        id: 'feelings_chart_inner',
        style: 'height:250px; margin-bottom: 1px;'
      }).appendTo('#feelings_chart');
      $('<div/>', {
        style: 'height: 10px;'
      }).appendTo('#stats');
      var feelings_chart = null;
      if (location.search.substring(1))
        feelings_chart = cf_feelings_percentages_last_hours(categories, dataset, names, 'Sentimentos escolhidos nas últimas 24 horas', 'feelings_chart_inner');
      else
        feelings_chart = cf_feelings_percentages_last_hours(categories, dataset, names, 'Sentimentos mais frequentes nas últimas 24 horas', 'feelings_chart_inner');
    }
}

function do_feelings_percentages_for_states(feelings_percentages_for_states) {
    for(var state in feelings_percentages_for_states) {
      if(feelings_percentages_for_states.hasOwnProperty(state)) {
        var fpfs = feelings_percentages_for_states[state];
        var categories = [];
        var dataset = [];
        for(var i=0; i<fpfs.length; i++) {
          categories.push(fpfs[i][0]);
          dataset.push(fpfs[i][1]);
        }
        var chart_id = 'states_charts_' + state;
        $('<div/>', {
          id: chart_id,
          class: 'charts-border'
        }).appendTo('#stats');
        $('<div/>', {
          id: chart_id + '_inner',
          style: 'height:250px; margin-bottom: 1px;'
        }).appendTo('#' + chart_id);
        $('<div/>', {
          style: 'height: 10px;'
        }).appendTo('#stats');
        var state_chart = cf_feelings_percentages_for_state(categories, dataset, getStateFromAbbreviation(state), chart_id + '_inner');
      }
    }
}

function do_weather_conditions_count_for_feelings(weather_conditions_count_for_feelings) {
    var categories = [];
    var dataset = [];
    var names = [];
    var colors = ['#2C476F', '#FCC047', '#AEAEAE', '#6B6B6B'];
    for(var i=0; i<weather_conditions_count_for_feelings.length; i++) {
      entry = weather_conditions_count_for_feelings[i];
      categories.push(entry[0]);
      for(var j=0; j<entry[1].length; j++) {
        if(i === 0) {
          dataset[j] = [];
          names.push(entry[1][j][0]);
        }
        dataset[j].push(entry[1][j][1]);
      }
    }
    $('<div/>', {
      id: 'weather_conditions_chart',
      class: 'charts-border'
    }).appendTo('#stats');
    $('<div/>', {
      id: 'weather_conditions_chart_inner',
      style: 'height:350px; margin-bottom: 1px;'
    }).appendTo('#weather_conditions_chart');
    $('<div/>', {
        style: 'height: 10px;'
    }).appendTo('#stats');
    var wc_chart = null;
    if (!location.search.substring(1))
      wc_chart = cf_weather_conditions_for_feelings(categories, dataset, names, colors, 'Condições climáticas para os sentimentos mais frequentes', 'weather_conditions_chart_inner');
    else
      wc_chart = cf_weather_conditions_for_feelings(categories, dataset, names, colors, 'Condições climáticas para os sentimentos ecolhidos', 'weather_conditions_chart_inner');

}
