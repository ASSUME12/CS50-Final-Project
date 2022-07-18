function GoToAssignment(tableName)
{
    var baseUrl =  window.location.origin;
    url = baseUrl + "/TestMe?tableName=" + tableName;
    window.location.href = url;
}
function GoToProgress(tableName)
{
    var baseUrl =  window.location.origin;
    url = baseUrl + "/Progress?tableName=" + tableName;
    window.location.href = url;
}


$(document).ready(function(){
    x = document.getElementsByClassName("row");
    Array.prototype.forEach.call(x, function(el) {
        el.setAttribute('data-after', '⮞');
    })

});

function showRows(id)
{
    idOld = id
    id = id + "2";
    x = document.getElementsByClassName(id)
    if (x[0].style.visibility != "visible")
    {
        document.getElementById(idOld).setAttribute('data-after', '⮟');
        elements = document.getElementsByClassName(id);
        Array.prototype.forEach.call(elements, function(el) {
            el.style.visibility = "visible";
            el.style.opacity = "1";
            el.style.position = "relative";
            el.style.left = "20px";  
        });
        
   }
   else
   {
        document.getElementById(idOld).setAttribute('data-after', '⮞');
        elements = document.getElementsByClassName(id);
        Array.prototype.forEach.call(elements, function(el) {
            el.style.visibility = "hidden";
            el.style.opacity = "0";
            el.style.position = "absolute";
        });
   }
   

}