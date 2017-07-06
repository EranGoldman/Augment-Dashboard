// fs = require('fs');




$(document).ready(function() {
    var getURL = "http://127.0.0.1:5000/conversations/" + "{{id}}" + "/get";
    $.getJSON(getURL, function(json) {
        console.log(json);
        var dataSet = json;
        var count2 = 0;
        while (dataSet[count2]) {
            count2++;
        }
        $('.title3').html(count2);
        console.log("got past");
        $('table#tableID').DataTable({
            "paging": true,
            "processing": true,
            // "ajax": '../DynamoDB/data.json',
            "data": dataSet,
            "columns": [
            { "data": "message_id" },
            { "data": "created_on" },
            ]
        });
        addRowHandlers();
    })
});

function addRowHandlers() {
    var table = document.getElementById("tableID");
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler =
            function(row)
            {
                return function() {
                                        var cell = row.getElementsByTagName("td")[1];
                                        var id = cell.innerHTML;
                                        var sessionViewURL = "http://127.0.0.1:5000/conversations/" + id;
                                                            // alert(sessionViewURL);
                                        window.open (sessionViewURL,'_self',false)
                                 };
            };

        currentRow.onclick = createClickHandler(currentRow);
    }
}
