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


function do_feelings_percentages_last_hours(feelings_percentages_last_hours) {
  var dataset = [];
  var names = [];
  var categories = [];
  var feelings_colors = [];
  for(var i=0; i<feelings_percentages_last_hours.length; i++) {
    entry = feelings_percentages_last_hours[i];
    if(i === 0) {
      for(var j=0; j<entry[1].length; j++) {
        var hours = entry[1][j];
        categories.push(hours[0]);
      }
    }
    names.push(entry[0]);
    feelings_colors.push(entry[2]);
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
      style: 'height: 250px; margin-bottom: 1px;'
    }).appendTo('#feelings_chart');
    $('<div/>', {
      style: 'height: 10px;'
    }).appendTo('#stats');
    var feelings_chart = null;
    if (location.search.substring(1))
      feelings_chart = cf_feelings_percentages_last_hours(categories, dataset, names, feelings_colors, 'Sentimentos escolhidos nas últimas 24 horas', 'feelings_chart_inner');
    else
      feelings_chart = cf_feelings_percentages_last_hours(categories, dataset, names, feelings_colors, 'Sentimentos mais frequentes nas últimas 24 horas', 'feelings_chart_inner');
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
        dataset.push({y: fpfs[i][1], color: fpfs[i][2]});
      }
      var chart_id = 'states_charts_' + state;
      $('<div/>', {
        id: chart_id,
        class: 'charts-border'
      }).appendTo('#stats');
      $('<div/>', {
        id: chart_id + '_inner',
        style: 'height: 250px; margin-bottom: 1px;'
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
  if(weather_conditions_count_for_feelings.length !== 0) {
    $('<div/>', {
      id: 'weather_conditions_chart',
      class: 'charts-border'
    }).appendTo('#stats');
    $('<div/>', {
      id: 'weather_conditions_chart_inner',
      style: 'height: 350px; margin-bottom: 1px;'
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
}

function do_feelings_percentages_and_mean_last_hours(feelings_percentages_and_mean_last_hour) {
  for(var i=0; i<feelings_percentages_and_mean_last_hour.length; i++) {
    var categories = [];
    var dataset = [];
    var names = [];
    var fpmlh = feelings_percentages_and_mean_last_hour[i];
    var dataset1 = [];
    var dataset2 = [];
    for(var j=0; j<fpmlh[1].length; j++) {
      dataset1.push(fpmlh[1][j][1]);
      dataset2.push(fpmlh[2][j][1]);
      categories.push(fpmlh[1][j][0]); // Inserting the hour eg.: 11, 12, 13
    }
    dataset.push(dataset1);
    dataset.push(dataset2);

    names.push(fpmlh[0]);
    names.push('média');

    var chart_id = 'feeling_mean_' + fpmlh[0];
    $('<div/>', {
      id: chart_id,
      class: 'charts-border'
    }).appendTo('#stats');
    $('<div/>', {
      id: chart_id + '_inner',
      style: 'height: 250px; margin-bottom: 1px;'
    }).appendTo('#' + chart_id);
    $('<div/>', {
      style: 'height: 10px;'
    }).appendTo('#stats');
    var feeling_mean_chart = cf_feelings_percentages_and_mean_last_hour(categories, dataset, names, fpmlh[3], chart_id + '_inner');
  }
}

function do_feelings_mean_percentages_every_two_hours(feelings_mean_percentages_every_two_hours) {
  $('<div/>', {
    id: 'test1',
    style: 'position:relative; display:table;'
  }).appendTo('#stats');
  var count = 0;
  var current_row = null;
  for(var i=0; i<feelings_mean_percentages_every_two_hours.length; i++) {
    if(i%5 === 0) {
      $('<div/>', {
        style: 'height: 10px;'
      }).appendTo('#test1');
      $('<div/>', {
        id: 'row' + count.toString(),
        style: 'display: table-row;'
      }).appendTo('#test1');
      current_row = '#row' + count.toString();
      count++;
    }
    var dataset = [];
    var categories = []; // Day hours
    var fmpeth = feelings_mean_percentages_every_two_hours[i];
    var day_color = ['#212433', '#4b495e', '#948790', '#f5c26c', '#e1ae45',
                     '#e78c39', '#e25621', '#e78c39', '#e1ae45', '#b3d2e4',
                     '#4877d3', '#263a77'];
    for(var j=0; j<fmpeth[1].length; j++) {
      dataset.push({y: fmpeth[1][j], color: day_color[j]});
      // dataset.push({y: fmpeth[1][j], color: fmpeth[2]});
      categories.push((j*2).toString() + '-' + ((j+1)*2).toString() + 'h');
    }

    var chart_id = 'feeling_radial_' + fmpeth[0];
    $('<div/>', {
      id: chart_id,
      // class: 'charts-border'
      style: 'display: table-cell; border: 1px solid #B9B9B9; background-color: #F9F9F9;'
    }).appendTo(current_row);
    $('<div/>', {
      id: chart_id + '_inner',
      style: 'height: 152px; width: 152px; margin-bottom: 1px;'
    }).appendTo('#' + chart_id);

    if((i+1)%5 !== 0) {
      $('<div/>', {
        style: 'display: table-cell; width: 10px;'
      }).appendTo(current_row);
    }
    var feeling_radial_chart = cf_feelings_mean_percentages_every_two_hours(categories, dataset, fmpeth[0], chart_id + '_inner', fmpeth[3]);
  }
  $('<div/>', {
    style: 'height: 10px;'
  }).appendTo('#stats');
}
