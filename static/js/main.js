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
            "order": [ 3, 'desc' ],
            "nowrap": true,
            // "ajax": '../DynamoDB/data.json',
            "data": dataSet,
            "columnDefs" : [ {
                    targets: 0,
                    render: function ( data, type, row )
                    {
                        return type === 'display' && data.length > 5 ?
                            data.substr( 0, 5 ) +'' :
                            data;
                    }
                    }],
            "columns": [
            {
                "data": "agentFullName",
                "width": "40px"
            },
            {
                "data": "engagementId",
                "width" : "160px"
            },
            {
                 "data": "chatLines",
                 "width" : "10%"
            },
            { "data": "startTime" },
            ]
        });
        $('table#tableID tbody').on('click', 'tr', function () {
          var data = table.row( this ).data();
          console.log(data);
          var sessionID = data["engagementId"];
          console.log(sessionID);
          var sessionViewURL = "http://127.0.0.1:5000/conversations/" + sessionID;
          console.log(sessionViewURL)
          window.open (sessionViewURL,'_self',false)
        })

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
