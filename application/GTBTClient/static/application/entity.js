function buildStatisticsPanel(stats){
    var classes = new Array();
    var counts = new Array();
    $("#stats-body").empty();
    for (var key in stats){
        
        classes.push(key);
        counts.push(stats[key]);
        //below we populate the table of classes.
        row = "<tr>"+"<td>"+key+"</td>"+"<td>"+stats[key]+"</td>"+"</tr>";
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
    
    /*build the option list*/
    $.each(dimensions, function() {$('#location-filter').append($("<option></option>").text(this).val(this));});
    
    /*make table*/
    $.each(JSON.parse(jsonData).slice(1, -1), function() {row = "<tr>"+"<td>"+this[0]+"</td>"+"<td>"+this[1]+"</td>"+"</tr>";$("#location-table").append(row);});
    
    drawGeoChart(JSON.parse(jsonData));
    
    window.onresize = function(event) {drawGeoChart(JSON.parse(jsonData));};
    
    $("#location-filter").change(function () {
                                 url =  "http://localhost:8888/entity/"+getUrlParameter("id")+"/dist/";
                                 if($('option:selected').text() != "all"){
                                    url = "http://localhost:8888/entity/"+getUrlParameter("id")+"/dist/?class="+$('#location-filter').val();
                                    console.log(url);
                                 }
                                 var jsonData = $.ajax({
                                                       url: url,
                                                       dataType: 'json',
                                                       async: false
                                                       }).responseText;
                                 var output = new Array();
                                 output = JSON.parse(jsonData);
                                 $("#location-table").empty();
                                 $.each(JSON.parse(jsonData).slice(1, -1), function() {row = "<tr>"+"<td>"+this[0]+"</td>"+"<td>"+this[1]+"</td>"+"</tr>";$("#location-table").append(row);});
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
                        url: "http://localhost:8888/entity/"+getUrlParameter("id")+"/disttime/",
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
function buildTweetsPanel(dimensions){
    $.getJSON("http://localhost:8888/entity/"+getUrlParameter("id")+"/tweets/")
        .done(function( tweets ){
             $.each(tweets, function() {
                   $("#tweets").append("<div class=\"panel panel-default panel-success\"><div class=\"panel-body\"> <span class=\"badge\">"+this['class']+"</span><blockquote>"+this['text']+"</blockquote></div><div class=\"panel-footer\"><small>created by: "+this['user']['screen_name']+", created at: "+this['created_at']+"</small></div></div>");
                    });
             });
    
    /*add event for dealing with the filtering of tweets by dimension.*/
    
    $.each(dimensions, function() {$('#tweet-filter').append($("<option></option>").text(this).val(this));});
    
    $("#tweet-filter").change(function () {
                              url =  "http://localhost:8888/entity/"+getUrlParameter("id")+"/tweets/";
                              if($('option:selected').text() != "all"){
                              url = "http://localhost:8888/entity/"+getUrlParameter("id")+"/tweets/?dimension="+$('#tweet-filter').val();
                              }
                              var jsonData = $.ajax({
                                                    url: url,
                                                    dataType: 'json',
                                                    async: false
                                                    }).responseText;
                              var output = new Array();
                              output = JSON.parse(jsonData);
                              /*empty the previous contents*/
                              $("#tweets").empty();
                              $.each(output, function() {
                                     $("#tweets").append("<div class=\"panel panel-default panel-success\"><div class=\"panel-body\"> <span class=\"badge\">"+this['class']+"</span><blockquote>"+this['text']+"</blockquote></div><div class=\"panel-footer\"><small>created by: "+this['user']['screen_name']+", created at: "+this['created_at']+"</small></div></div>");
                                     });
                              })
}

function buildPage(entity_data){
   
    buildStatisticsPanel(entity_data['stats']);
    buildTweetsPanel(entity_data['classes']);
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

$('#btnTrack').click(function(){
                     token = $("[name=csrfmiddlewaretoken]").val();
                     if($('#btnTrack').val() == "Track"){
                     
                     
                        $.ajax({
                               type: "POST",
                               url: "http://localhost:8000/app/addtrack/",
                               data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': token},
                               dataType: "text",
                               success: function(response) {
                               $("<div class=\"alert alert-success alert-dismissible\" role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button><strong>Success!</strong>Removed Track from Personal Track List</div>").prependTo('body').hide().fadeIn('fast');                               $("#pgtitle").append("<span id=\"trackicon\" class=\"glyphicon glyphicon-ok-circle\"style=\"color:Lime\" aria-hidden=\"true\"></span>");
                               $('#btnTrack').val("Untrack");
                               },
                               error: function(rs, e) {}
                               });
                     }else{
                    
                     $.ajax({
                            type: "POST",
                            url: "http://localhost:8000/app/untrack/",
                            data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': token},
                            dataType: "text",
                            success: function(response) {
                            $("<div class=\"alert alert-success alert-dismissible\" role=\"alert\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button><strong>Success!</strong>Removed Track from Personal Track List</div>").prependTo('body').hide().fadeIn('fast');
                            $("#trackicon").remove();
                            $('#btnTrack').val("Track");
                            },
                            error: function(rs, e) {}
                            });
                     }
                    
                        })
$("#btnSearch").click(function(event) {
                      var v = $("#searchBox").val();
                      window.location ="/app/entity/?id="+v;
                      });
function esd(){
    $("#container").empty();
    $("body").append("<div class=\"container\"><div class=\"jumbotron\"><h1>404: Entity does not exist!</h1><p>The entity you were looking for is not in the GTBT system. To add it go to the user menu and select \"Add Entity\".</p></div></div>");
}
/*main routine*/
$(document).ready(function(){
                  $.getJSON("http://localhost:8888/entity/"+getUrlParameter("id")).done(function( json ) {buildPage(json);}).fail(function() {
                                                                                                                                  esd();
                                                                                                                                  });
                  //$('#btnAddTrack').val = getUrlParameter("id");
                  $(function () {$('[data-toggle="tooltip"]').tooltip()});
                 
});
