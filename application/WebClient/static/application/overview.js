
function buildPage(data){
    buildTimePanel();
    
}
function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}
function buildTimePanel(){
    var output = $.ajax({
                        url: "http://localhost:8888/entity/BMW/disttime/",
                        dataType: 'json',
                        async: false
                        }).responseText;
    var timedistribution = JSON.parse(output);
    drawLineChart(timedistribution);
    window.onresize = function(event) {drawLineChart(timedistribution);};
}
google.load("visualization", "1", {packages:["corechart"]});
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
    dataArray.sort(sortFunction);
    data.addRows(dataArray);
    
    
    
    // Set chart options
    var options = {};
    
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('growth-chart'));
    chart.draw(data, options);
}



$(document).ready(function(){
                  url = "http://localhost:8888/entities/";
                  $.getJSON(url,function(data) { buildPage(data);});
                  
                  });
                 