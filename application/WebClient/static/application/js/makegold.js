function makeGold(string){
    console.log(string);
    $.post( "http://localhost:9000/makegold/", {"id":string}, function() {
           }).fail(function() {
                   alert( "error" );
                   })
}