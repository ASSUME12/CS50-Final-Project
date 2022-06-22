function AddVokabulariesInputs()
{
    var url_string = window.location.href;
    var url = new URL(url_string);
    var tableName = url.searchParams.get("tableName");


    var Vokabularies;
    fetch('/getTestMeData?tableName=' + tableName, {method: 'POST', body: 'getTestMeData?tableName'}).then(response => response.json()).then(function(data){
        var Vokabularies = [];
        Vokabularies = data["data"];
        var vokabularysInputs = document.getElementById("vokabularysInputs");

        var div = document.createElement("div");
        var div1 = document.createElement("div");
        var div2 = document.createElement("div");
        var div3 = document.createElement("div");
        var div4 = document.createElement("div");
        div.className = "sglspread";
        div1.className = "text-holder right";
        div2.className = "pg1-2-txt TestMeLanguage";
        div3.className = "text-holder left";
        div4.className = "pg1-2-txt TestMeLanguage";


        var legend = document.createElement("legend");
        legend.className = "border-bottom mb-4"; 

        var FirstLanguageSpan = document.createElement("span");
        var SecondLanguageSpan = document.createElement("span");

        FirstLanguageSpan.innerHTML =  data["firstLanguage"];
        SecondLanguageSpan.innerHTML = data["secondLanguage"];

        SecondLanguageSpan.id = "SecondLanguageSpan";

        legend.appendChild(FirstLanguageSpan);
        legend.appendChild(SecondLanguageSpan);
        div.appendChild(div1);
        div1.appendChild(div2);
        div2.appendChild(SecondLanguageSpan);
        div.appendChild(div3);
        div3.appendChild(div4);
        div4.appendChild(FirstLanguageSpan);

        vokabularysInputs.appendChild(div);

        document.getElementById("tableIdentidfier").value = tableName;

        for (let index = 0; index < Vokabularies.length; index++) {
            var div1 = document.createElement("div");

            var input1 = document.createElement("input");
            input1.id = "lang1" + index;
            input1.className = "lang1" + index + " lang1";
            input1.name = "lang1" + index
            input1.autocomplete = "off";
            var vokablurayFirstLanguage = Vokabularies[index]["firstVokabulary"]
            input1.value = vokablurayFirstLanguage;
            input1.readOnly  = true;

            var input2 = document.createElement("input");
            input2.id = "lang2" + index;
            input2.className = "lang2" + index + " lang2";
            input2.name = "lang2" + index
            input2.autocomplete = "off";


            div1.id = "lang1" + index + " div";
            div1.appendChild(input1);
            div1.appendChild(input2);

            vokabularysInputs.appendChild(div1);
        }
    });
    
}
function GoHome()
{
    window.location.href = "/";
}


