function GoToAssignment(tableName)
{
    url = "http://127.0.0.1:5000/TestMe?tableName=" + tableName;
    window.location.href = url;
}
function GoToProgress(tableName)
{
    url = "http://127.0.0.1:5000/Progress?tableName=" + tableName;
    window.location.href = url;
}
