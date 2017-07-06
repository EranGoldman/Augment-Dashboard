// fs = require('fs');




$(document).ready(function() {
    $.getJSON("http://127.0.0.1:5000/conversations", function(json) {
        console.log(json);
        var dataSet = json;
        var count2 = 0;
        while (dataSet[count2]) {
            count2++;
        }
        $('.title3').html(count2);
        console.log("got past");
        var table = $('table#tableID').DataTable({
            "paging": true,
            "processing": true,
            // "ajax": '../DynamoDB/data.json',
            "data": dataSet,
            "columns": [
            { "data": "agentFullName" },
            { "data": "engagementId" },
            { "data": "chatLines" },
            { "data": "startTime" },
            ]
        });
        $('table#tableID tbody').on('click', 'tr', function () {
          var data = table.row( this ).data();
          console.log(data);
          var sessionID = data["engagementId"];
          var sessionViewURL = "http://127.0.0.1:5000/conversations/" + sessionID;
          alert(sessionViewURL);
          window.open (sessionViewURL,'_self',false)
        })
        // addRowHandlers();
    })
});



// function addRowHandlers() {
//     var table = document.getElementById("tableID");
//     var rows = table.getElementsByTagName("tr");
//     for (i = 0; i < rows.length; i++) {
//         var currentRow = table.rows[i];
//         var createClickHandler =
//             function(row)
//             {
//                 return function() {
//                                         var cell = row.getElementsByTagName("td")[1];
//                                         var id = cell.innerHTML;
//                                         var sessionViewURL = "http://127.0.0.1:5000/conversations/" + id;
//                                         alert(sessionViewURL);
//                                         window.open (sessionViewURL,'_self',false)
//                                  };
//             };
//
//         currentRow.onclick = createClickHandler(currentRow);
//     }
// }
