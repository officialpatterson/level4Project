google.load("visualization", "1", {packages:["geochart", "corechart"]});

function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}
function tweetRatePanel(entity){
    $.getJSON("http://localhost:9000/api/timedistribution/",{"entity":entity},function(timedistribution) {
  
        
        drawLineChart(timedistribution);
        window.onresize = function(event) {drawLineChart(timedistribution);};
    }); //end getJSON
}
function drawLineChart(timedistribution){
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'time');
    data.addColumn('number', 'tweets');
    timedistribution.shift();
    
    var dataArray = new Array();
    
    $.each(timedistribution, function() {
           
           dataArray.push([new Date(this[0]), this[1]]);
           });
    count = 0;
    $.each(timedistribution, function() {
           
           dataArray.push([new Date(this[0]), count]);

           });
    dataArray.sort(sortFunction);
    data.addRows(dataArray);
    
    
    
    // Set chart options
    var options = {};
    
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('TimeChart'));
    chart.draw(data, options);
}
function dimensionDistributionPanel(entity){
    $.getJSON("http://localhost:9000/api/dimensiondistribution/",{"entity":entity},function(dimensions) {
              
              $("#stats-body").empty();
              classes = new Array();
              counts = new Array();
              for (var key in dimensions){
                  
                  //below we populate the table of classes.
                  row = "<tr>"+"<td>"+key+"</td>"+"<td>"+dimensions[key]+"</td>"+"</tr>";
                  $("#stats-body").append(row);
              
                classes.push(key);
                counts.push(dimensions[key]);

              }
              
              var data = {
              labels: classes,
              datasets: [
                         {
                         label: "class stats",
                         fillColor: "rgba(151,187,205,0.5)",
                         strokeColor: "rgba(151,187,205,0.8)",
                         highlightFill: "rgba(151,187,205,0.75)",
                         highlightStroke: "rgba(151,187,205,1)",
                         data: counts
                         }
                         ]
              };
              Chart.defaults.global.responsive = true;
              //Chart.defaults.global.responsive = true;
              var ctx = document.getElementById("myChart").getContext("2d");
              var myBarChart = new Chart(ctx).Bar(data);
              
    }); //end getJSON
}

function drawGeoChart(dimension){
    var data = google.visualization.arrayToDataTable(dimension);
    var options = {};
    
    var chart = new google.visualization.GeoChart(document.getElementById('locationChart'));
    chart.draw(data, options);
}
function LocationDistributionPanel(entity){
    $.getJSON("http://localhost:9000/api/locationdistribution/",{"entity":entity},function(dimensions) {
              
              /*build the option list*/
              $.each(dimensions, function() {$('#location-filter').append($("<option></option>").text(this).val(this));});
              
              
              drawGeoChart(dimensions);
              
              
              window.onresize = function(event) {drawGeoChart(dimensions);};

    }); //end getJSON
};
function BeforeLastPartofURL() {
    var url = window.location.href;
    var parts = url.split("/");
    var beforeLast = parts[parts.length - 2]; //keep in mind that since array starts with 0, last part is [length - 1]
    return beforeLast;
}
$(document).ready(function(){
                  entity = BeforeLastPartofURL()
                  dimensionDistributionPanel(entity);
                  LocationDistributionPanel(entity);
                  tweetRatePanel(entity);
                  });
