
function buildPage(){
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
    var timeportion=24;
    renderLineChart(timeportion);
    
    window.onresize = function(event) {renderLineChart(timeportion);};
    
    $('#time-filter').on('change', function (e) {
                         console.log(this.value);
                  renderLineChart(this.value);
                    
                   });
}
function renderLineChart(intervals){
    $.getJSON("http://localhost:9000/api/timedistribution/",{"division":intervals},function(timedistribution) {
              
              
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
    var chart = new google.visualization.LineChart(document.getElementById('growth-chart'));
    chart.draw(data, options);
}
google.load("visualization", "1", {packages:["corechart"]});



$(document).ready(function(){
                  buildPage();
            
                  });
                 