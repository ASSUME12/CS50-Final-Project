$(document).ready(function(){


  $("#serchBox").on("input", function(){
    fetch("http://127.0.0.1:5000/searchForUsers?username=" + $("#serchBox").val(), {method: 'POST', body: 'searchForUsers'}).then(response => response.json()).then(function(usersData){
      users = usersData["users"]

      var container = document.getElementById("search-scrollbar")
      while (container.lastElementChild) {
        container.removeChild(container.lastElementChild);
      }

      for (let index = 0; index < users.length; index++)
      {
          var a = document.createElement("a");
          a.href = "/" + users[index]["username"];
          a.style.textDecoration = "none";
          var user_itemDiv = document.createElement("div");
          user_itemDiv.className = "user_item";
          var user_imgDiv = document.createElement("div");
          user_imgDiv.className = "user_img";
          var profile_pic = document.createElement("img");
          profile_pic.src = "/static/profile_pics/" + users[index]["profile_pic"];
          profile_pic.style.width = "50px";

          user_imgDiv.appendChild(profile_pic);
          user_itemDiv.appendChild(user_imgDiv);

          var user_infoDiv = document.createElement("div");
          user_infoDiv.className = "user_info";
          var p = document.createElement("p");
          p.innerHTML = users[index]["username"];
          var span = document.createElement("span");
          span.innerHTML = users[index]["role"]

          p.appendChild(span);
          user_infoDiv.appendChild(p);

          user_itemDiv.appendChild(user_infoDiv);
          a.appendChild(user_itemDiv);
          document.getElementById("search-scrollbar").appendChild(a);

          var active = $('.search-dropdown').hasClass("active");
          if (!active)
          {
            $(".search-dropdown").toggleClass("active");
          }
      }

      if (users.length == 0)
      {
        var user_itemDiv = document.createElement("div");
          user_itemDiv.className = "user_item";
          var user_imgDiv = document.createElement("div");
          user_imgDiv.className = "user_img";
         
          user_itemDiv.appendChild(user_imgDiv);

          var user_infoDiv = document.createElement("div");
          user_infoDiv.className = "user_info";
          var p = document.createElement("p");
          p.innerHTML = "No users found!";

          user_infoDiv.appendChild(p);

          user_itemDiv.appendChild(user_infoDiv);
          document.getElementById("search-scrollbar").appendChild(user_itemDiv);

          var active = $('.search-dropdown').hasClass("active");
          if (!active)
          {
            $(".search-dropdown").toggleClass("active");
          }
      }
      else if (usersData["users"] == -1)
      {
          var active = $('.search-dropdown').hasClass("active");
          if (active)
          {
            $(".search-dropdown").toggleClass("active");
          }
      }

  });
});


  fetch("http://127.0.0.1:5000/getNotificationsNumber" , {method: 'POST', body: 'getNotificationsNumber'}).then(response => response.json()).then(function(data){
    document.getElementById("wrapper").setAttribute('data-value', data["notificationsNumber"]);
    
    if (data["notificationsNumber"] != 0)
    {
      $(".wrapper").toggleClass("notifications");
    }

  });

  $(document).click(function(event) {

    if (!$(event.target).closest('.notification_icon .fa-bell').length && !$(event.target).closest('#profile').length && !$(event.target).closest('#search').length) {
      var active = $('.dropdown').hasClass("active");
      if (active)
      {
        $(".dropdown").toggleClass("active");
      }
      var active = $('#menu').hasClass("active");
      if (active)
      {
        $("#menu").toggleClass("active");
      }
      var active = $('.search-dropdown').hasClass("active");
      if (active)
      {
        $(".search-dropdown").toggleClass("active");
      }
    }
    
    
    
  });
    $("#profile" ).click(function() {
        $("#menu").toggleClass("active");
        var active = $('.dropdown').hasClass("active");
        if (active)
        {
          $(".dropdown").toggleClass("active");
        }
        var active = $('.search-dropdown').hasClass("active");
        if (active)
        {
          $(".search-dropdown").toggleClass("active");
        }
      });
    $(".notification_icon .fa-bell").click(function(){
      $(".dropdown").toggleClass("active");
      fetch('http://127.0.0.1:5000/setnotificationsAlreadyRead' , {method: 'POST', body: 'setnotificationsAlreadyRead'}).then(response => response.json()).then(function(data){
        document.getElementById("wrapper").setAttribute('data-value', data["notificationsNumber"]);
        if ($('.wrapper').hasClass("notifications"))
        {
          $(".wrapper").toggleClass("notifications");
        }
       
      });
      var active = $('#menu').hasClass("active");
      if (active)
      {
        $("#menu").toggleClass("active");
      }
      var active = $('.search-dropdown').hasClass("active");
      if (active)
      {
        $(".search-dropdown").toggleClass("active");
      }
    })
});



