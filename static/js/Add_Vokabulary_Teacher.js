function indexOfVokabularyChanged(numberOfVokabularies)
{
    var vokabularysInputs = document.getElementById("vokabularysInputs");
    

    while (vokabularysInputs.lastElementChild) {
        vokabularysInputs.removeChild(vokabularysInputs.lastElementChild);
      }

    var div = document.createElement("div");
    var div1 = document.createElement("div");
    var div2 = document.createElement("div");
    var div3 = document.createElement("div");
    var div4 = document.createElement("div");
    div.className = "sglspread";
    div1.className = "text-holder right";
    div2.className = "pg1-2-txt";
    div3.className = "text-holder left";
    div4.className = "pg1-2-txt";


    var legend = document.createElement("legend");
    legend.className = "border-bottom mb-4"; 

    var FirstLanguageSpan = document.createElement("span");
    var firstLanguage = document.getElementById("firstLanguage");
    if (firstLanguage.value != "")
    {
        FirstLanguageSpan.innerHTML = firstLanguage.value;
    }
    else{
        FirstLanguageSpan.innerHTML = "First Language";
    }
    
    FirstLanguageSpan.id = "FirstLanguageSpan";

    var SecondLanguageSpan = document.createElement("span");
    var secondLanguage = document.getElementById("secondLanguage");
    if (secondLanguage.value != "")
    {
        SecondLanguageSpan.innerHTML = secondLanguage.value;
    }
    else{
        SecondLanguageSpan.innerHTML = "Second Language";
    }
    
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

    for (let index = 0; index < numberOfVokabularies; index++) {
        var div1 = document.createElement("div");

        var input1 = document.createElement("input");
        input1.id = "lang1" + index + " lang1";
        input1.name = "lang1" + index
        input1.autocomplete = "off";

        var input2 = document.createElement("input");
        input2.id = "lang2" + index + " lang2";
        input2.name = "lang2" + index
        input2.autocomplete = "off";

        var close_button1 = document.createElement("button");
        close_button1.className = "close";
        close_button1.type = "button";
        var close_button1_span = document.createElement("span");
        close_button1_span.innerHTML = "Delete"; //&times;
        close_button1_span.ariaHidden = true;
        close_button1_span.id = "close_button1_span";
        //close_button1_span.style.color = "floralwhite";
        close_button1.setAttribute( "onClick", "removeVokabularyInput(this.id)" );
        close_button1.appendChild(close_button1_span);
        close_button1.id = "lang1" + index;
        div1.id = "lang1" + index + " div";
        div1.appendChild(input1);
        div1.appendChild(input2);
        div1.appendChild(close_button1);

        

        

        vokabularysInputs.appendChild(div1);
    }
}

function removeVokabularyInput(id)
{
    var vokabularyDiv = document.getElementById(id + " div");
    vokabularyDiv.remove();
}

function FirstLanguageChaged(language)
{
    var firtsLanguageSpan = document.getElementById("FirstLanguageSpan");

    if (language != "")
        {
            firtsLanguageSpan.innerHTML = language;
        }
        else
        {
            firtsLanguageSpan.innerHTML = "First Language";
        }
    
}


function SecondLanguageChaged(language)
{
    var SecondLanguageSpan = document.getElementById("SecondLanguageSpan");

    if (SecondLanguageSpan != null)
    {   
        if (language != "")
        {
            SecondLanguageSpan.innerHTML = language;
        }
        else
        {
            SecondLanguageSpan.innerHTML = "Second Language";
        }
        
    }
}