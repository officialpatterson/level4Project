
function buildEntityList(data){
    for (i = 0; i < data.length; i++){
        row = "<tr><td><a href=\"/app/entity/?id="+data[i]+"\">"+data[i]+"</a></td></tr>";
        $("#entities-body").append(row);
    }
}
function buildCollectionSummaryPanel(data){
    $("#panel-summary").append("<p>Number Entities: "+data['entities'].length+ "</p>");
    $("#panel-summary").append("<p>Number of Dimensions: "+data['dimensions'].length+ "</p>");
    $("#panel-summary").append("<p>Size of Collection: "+data['size']+ "</p>");
}
function buildPage(data){
    buildEntityList(data['entities'])
    buildTimePanel();
    buildCollectionSummaryPanel(data);
    
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
$("#btnSearch").click(function(event) {
                    var v = $("#searchBox").val();
                   window.location ="entity/?id="+v;
                   });

$(document).ready(function(){
                  url = "http://localhost:8888/entities/";
                  $.getJSON(url,function(data) { buildPage(data);});
                  
                  var notCount = $.ajax({
                                      url: "http://localhost:8000/app/notifications/",
                                      dataType: 'json',
                                      async: false
                                      }).responseText;
                  $("#notifications").append(" <span class=\"badge\">"+notCount+"</span></a>");
                  $("#menu").append(" <span class=\"badge\">"+notCount+"</span></a>");
                  });