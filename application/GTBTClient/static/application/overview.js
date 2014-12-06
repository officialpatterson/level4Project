
function buildEntityList(data){
    for (i = 0; i < data.length; i++){
        row = "<tr><td><a href=\"/app/entity/?id="+data[i]+"\">"+data[i]+"</a></td></tr>";
        $("#entities-body").append(row);
    }
}
function buildPage(data){
    buildEntityList(data['entities'])
    $("#panel-summary").append("Size of Collection: "+data['size'])
}

$(document).ready(function(){
                  url = "http://localhost:8888/entities/";
                  $.getJSON(url,function(data) { buildPage(data);});
                  });