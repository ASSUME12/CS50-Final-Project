function SelectChanged(value)
{
    groupNumberDiv = document.getElementById("GroupnumberDiv")
    if (value == "Teacher")
    {
        groupNumberDiv.style.visibility = "hidden";
    }
    else if (value == "Student")
    {
        groupNumberDiv.style.visibility = "visible";
    }
}