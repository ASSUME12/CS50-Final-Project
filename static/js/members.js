function AcceptUser(id)
{
    document.getElementById(id+"acceptInput").value = id;
    document.getElementById(id+"AcceptForm").submit();
}

function DeclineUser(id)
{
    document.getElementById(id+"declineInput").value = id;
    document.getElementById(id+"DeclineForm").submit();
}