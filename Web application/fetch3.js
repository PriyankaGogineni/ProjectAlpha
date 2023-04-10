//To display the data received from the callRekApi() function in the format provided in the HTML code snippet, you need to modify the function to update the values of the table cells in the HTML page. Here's an example of how you can achieve this:

function callRekApi(photo) {
    var xhr = new XMLHttpRequest();
    var url = "http://http://127.0.0.1:5000/get-s3-data";
    var params = "object_key=" + photo;
    xhr.open('GET', url + "?" + params, true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText).data;
        
        // Update today's data
        document.getElementById("today-paper").textContent = data.today.paper;
        document.getElementById("today-plastic").textContent = data.today.plastic;
        document.getElementById("today-glass").textContent = data.today.glass;
        document.getElementById("today-metal").textContent = data.today.metal;
        document.getElementById("today-cardboard").textContent = data.today.cardboard;
        
        // Update yesterday's data
        document.getElementById("yesterday-paper").textContent = data.yesterday.paper;
        document.getElementById("yesterday-plastic").textContent = data.yesterday.plastic;
        document.getElementById("yesterday-glass").textContent = data.yesterday.glass;
        document.getElementById("yesterday-metal").textContent = data.yesterday.metal;
        document.getElementById("yesterday-cardboard").textContent = data.yesterday.cardboard;
        
        // Update last week's data
        document.getElementById("lastweek-paper").textContent = data.lastweek.paper;
        document.getElementById("lastweek-plastic").textContent = data.lastweek.plastic;
        document.getElementById("lastweek-glass").textContent = data.lastweek.glass;
        document.getElementById("lastweek-metal").textContent = data.lastweek.metal;
        document.getElementById("lastweek-cardboard").textContent = data.lastweek.cardboard;
      }
    };
    xhr.send();
  }
  


