function buildStatisticsPanel(){
    
    /*get first entity data*/
    var response = $.ajax({
                          url: "http://localhost:8888/entity/"+getUrlParameter("eidone"),
                          dataType: 'json',
                          async: false
                          }).responseText;
    var json = JSON.parse(response);
    var eonestats = json['stats'];
    
    /*get second entity data*/
    var response = $.ajax({
                          url: "http://localhost:8888/entity/"+getUrlParameter("eidtwo"),
                          dataType: 'json',
                          async: false
                          }).responseText;
    var json = JSON.parse(response);
    var etwostats = json['stats'];
    
    var classes = new Array();
    var countsFirstEntity = new Array();
    var countsSecondEntity = new Array();
    $("#stats-body").empty();
    
    
    /*process first dataset*/
    for (var key in eonestats){
        classes.push(key)
        countsFirstEntity.push(eonestats[key])
        //below we populate the table of classes.
        row = "<tr>"+"<td>"+key+"</td>"+"<td>"+eonestats[key]+"</td>"+"</tr>"
        $("#stats-body").append(row);
    }
  
     
     /*process second dataset*/
    for (var key in etwostats){
        if( $.inArray(key, classes) == -1){
            classes.push(key)
        }
        
        countsSecondEntity.push(etwostats[key])
        //below we populate the table of classes.
        row = "<tr style=\"color:red\">"+"<td>"+key+"</td>"+"<td>"+etwostats[key]+"</td>"+"</tr>"
        $("#stats-body").append(row);
    }
    
    classes = $.unique(classes);
    console.log(classes.length);
    var data = {
    labels: classes,
    datasets: [
               {
               label: getUrlParameter("eidone"),
               fillColor: "rgba(151,187,205,0.5)",
               strokeColor: "rgba(151,187,205,0.8)",
               highlightFill: "rgba(151,187,205,0.75)",
               highlightStroke: "rgba(151,187,205,1)",
               data: countsFirstEntity
               },
               {
               label: getUrlParameter("eidtwo"),
               fillColor: "rgba(220,220,220,0.5)",
               strokeColor: "rgba(220,220,220,0.8)",
               highlightFill: "rgba(220,220,220,0.75)",
               highlightStroke: "rgba(220,220,220,1)",
               data: countsSecondEntity
               }
               ]
    };
    Chart.defaults.global.responsive = true;
    //Chart.defaults.global.responsive = true;
    var ctx = document.getElementById("myChart").getContext("2d");
    var myBarChart = new Chart(ctx).Bar(data);
    
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
function initialiseFormComponents(){
    url = "http://localhost:8888/entities/";
    $.getJSON(url,function(data) {
              
              $.each(data['entities'],function(){$("#FirstEntity").append($("<option></option>").text(this).val(this));});
              $.each(data['entities'],function(){$("#secondEntity").append($("<option></option>").text(this).val(this));});
              });
}
/*main routine*/
$(document).ready(function(){
    initialiseFormComponents();
    buildStatisticsPanel();

});
function submitForm(){
    var eid1 = $( "#FirstEntity" ).val();
    var eid2 = $( "#secondEntity" ).val();
    window.location.replace("http://localhost:8000/app/compare/?eidone="+eid1+"&&eidtwo="+eid2);
}