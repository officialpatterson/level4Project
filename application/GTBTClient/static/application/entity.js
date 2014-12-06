function buildStatisticsPanel(stats){
    var classes = new Array();
    var counts = new Array();
    $("#stats-body").empty();
    for (var key in stats){
        
        classes.push(key)
        counts.push(stats[key])
        //below we populate the table of classes.
        row = "<tr>"+"<td>"+key+"</td>"+"<td>"+stats[key]+"</td>"+"</tr>"
        $("#stats-body").append(row);
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
    
}
function buildLocationPanel(dimensions){
    var jsonData = $.ajax({
                          url: "http://localhost:8888/entity/"+getUrlParameter("id")+"/dist/",
                          dataType: 'json',
                          async: false
                          }).responseText;
    
    $.each(dimensions, function() {
           $('#location-filter').append(
                                    $("<option></option>").text(this).val(this)
                                    );
           });
    var output = new Array();
    output = JSON.parse(jsonData);
    drawGeoChart(output);
    
    window.onresize = function(event) {drawGeoChart(output);};
    
    $("#location-filter").change(function () {
                                 url =  "http://localhost:8888/entity/"+getUrlParameter("id")+"/dist/";
                                 if($('option:selected').text() != "all"){
                                 url = "http://localhost:8888/entity/"+getUrlParameter("id")+"/dist/?class="+$('option:selected').text();
                                 }
                                 var jsonData = $.ajax({
                                                       url: url,
                                                       dataType: 'json',
                                                       async: false
                                                       }).responseText;
                                 var output = new Array();
                                 output = JSON.parse(jsonData);
                                 drawGeoChart(output);
                                 })
};
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
google.load("visualization", "1", {packages:["geochart", "corechart"]});
function drawLineChart(timedistribution){
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'time');
    data.addColumn('number', 'tweets');
 
    timedistribution.shift();
    console.log(timedistribution.length);
    var dataArray = new Array();
    
    $.each(timedistribution, function() {
           
           dataArray.push([new Date(this[0]), this[1]]);
           });
    dataArray.sort(sortFunction);
    data.addRows(dataArray);
    
    
    
    // Set chart options
    var options = {};
    
    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('TimeChart'));
    chart.draw(data, options);
}
function drawGeoChart(data) {
    var data = google.visualization.arrayToDataTable(data);
    var options = {};
    
    var chart = new google.visualization.GeoChart(document.getElementById('locationChart'));
    chart.draw(data, options);
}
function buildTweetsPanel(){
    $.getJSON("http://localhost:8888/entity/"+getUrlParameter("id")+"/tweets/")
        .done(function( tweets ){
             $.each(tweets, function() {
                   $("#panel-tweets-body").append("<div class=\"panel panel-default panel-success\"><div class=\"panel-body\"> <span class=\"badge\">"+this['class']+"</span><blockquote>"+this['text']+"</blockquote></div><div class=\"panel-footer\"><small>created by: "+this['user']['screen_name']+", created at: "+this['created_at']+"</small></div></div>");
                    });
             });
    
    
}

function buildPage(entity_data){
    $("#pgtitle").html(entity_data['entity']);
    buildStatisticsPanel(entity_data['stats']);
    buildTweetsPanel();
    buildTimePanel();
    buildLocationPanel(entity_data['classes']);
}
function getUrlParameter(sParam){
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
}


         
/*main routine*/
$(document).ready(function(){
    $.getJSON("http://localhost:8888/entity/"+getUrlParameter("id")).done(function( json ) {buildPage(json);});
                  
    $(function () {$('[data-toggle="tooltip"]').tooltip()})
});
