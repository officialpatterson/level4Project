function pushPin(string){
    console.log(string);
    $.post( "http://localhost:9000/pushpin/", {"id":string}, function() {
           }).fail(function() {
                   alert( "error" );
                   })
}