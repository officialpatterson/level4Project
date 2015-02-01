timeperiod = $("#timeperiod").val();
google.load("visualization", "1", {packages:["geochart", "corechart"]});

function tweetRatePanel(entity, dimension){
    console.log(dimension);
    $.getJSON("http://localhost:9000/api/timedistribution/",{"entity":entity, "period":timeperiod, "dimension":dimension},function(timedistribution) {
  
        
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

    data.addRows(dataArray);
    
    
    
    // Set chart options
    var options = {};
    
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('TimeChart'));
    chart.draw(data, options);
}

function drawGeoChart(dimension){
    var data = google.visualization.arrayToDataTable(dimension);
    var options = {};
    
    var chart = new google.visualization.GeoChart(document.getElementById('locationChart'));
    chart.draw(data, options);
}
function LocationDistributionPanel(entity, dimension){
    $.getJSON("http://localhost:9000/api/locationdistribution/",{"entity":entity, "period": timeperiod, "dimension":dimension},function(dimensions) {
              
              /*build the option list*/
              $.each(dimensions, function() {$('#location-filter').append($("<option></option>").text(this).val(this));});
              
              
              drawGeoChart(dimensions);
              
              
              window.onresize = function(event) {drawGeoChart(dimensions);};

    }); //end getJSON
};
function getEntityNameFromUrl(string) {
    var url = window.location.href;
    var parts = url.split("/");
    var entity = parts[parts.length - 3];
    return entity
}
function getDimensionNameFromUrl(string) {
    var url = window.location.href;
    var parts = url.split("/");
    var entity = parts[parts.length - 2];
    return entity
}
$(document).ready(function(){
                  entity = getEntityNameFromUrl();
                  dimension = getDimensionNameFromUrl();
                  LocationDistributionPanel(entity, dimension);
                  tweetRatePanel(entity, dimension);
                  });
