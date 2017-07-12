// fs = require('fs');




$(document).ready(function() {
    // downloading full table without filters
    var currentURL = $(location).attr('href');
    htmlSessionid = appConfig.htmlSessionID
    var getURL = "http://127.0.0.1:5000/conversations/" + htmlSessionid + "/get";
    console.log(getURL);
    var table;
    $.getJSON(getURL, function(json) {
        console.log(json);
        var dataSet = json;
        var count2 = 0;
        while (dataSet[count2]) {
            count2++;
        }
        $('.title3').html(count2);
        console.log("got past");
        table = $('table#tableID2').DataTable({
            "paging": true,
            "processing": true,
            "data": dataSet,
            "nowrap": true,
            "columns": [
                {
                    "data": "lineSeq",
                    "width": "24px"
                },
                {
                    "data": "lineText",
                    "width":"498px"
                },
            ]
        });
        $('table#tableID23 tbody').on('click', 'tr', function () {
            //use this code to go down to the state level
            var data = table.row( this ).data();
            console.log(data);
            //   var sessionID = data["engagementId"];
            //   var sessionViewURL = "http://127.0.0.1:5000/conversations/" + sessionID;
            //   window.open (sessionViewURL,'_self',false)
        })
    })

    // Updating table based on filter checkboxes
    $("input[type='checkbox']").change(function()
    {
        var filterArray = [];
        $('input[name="filter"]:checked').each(function()
        {
            filterArray.push($(this).val());
            console.log(filterArray);
        });
        var filterArrayLength = filterArray.length;
        var sessionID1 = htmlSessionid;
        var filteredURL = "http://127.0.0.1:5000/conversations/" + sessionID1 + "/filter/";
        console.log(filteredURL);
        for (var i = 0; i < filterArrayLength; i++)
        {
            filteredURL = filteredURL + "?";
            filteredURL = filteredURL + filterArray[i];
            filteredURL = filteredURL + "=1";
        }
        $.getJSON(filteredURL, function(json) {
            console.log(json);
            var dataSet = json;
            var count2 = 0;
            while (dataSet[count2]) {
                count2++;
            }

            $('.title3').html(count2);
            console.log("size of requested json array:" + count2);
            if(count2 != 0)
            {
                table.destroy();
                if(json[0].hasOwnProperty("lineSeq"))//checking staging_chat_lines
                {
                    console.log("Pulling from Prod_Chat_Lines Table -- only")
                    table = $('table#tableID2').DataTable({
                        "destroy": true,
                        "paging": true,
                        "processing": true,
                        "data": dataSet,
                        "columns": [
                            { "data": "lineSeq" },
                            { "data": "lineText" },
                        ]
                    });
                }
                else if(json[0].hasOwnProperty("intent")) //checking prod_augment_response
                {
                    table = $('table#tableID2').DataTable({
                        "destroy": true,
                        "paging": true,
                        "processing": true,
                        "data": dataSet,
                        "columns": [
                            { "data": "message_id" },
                            { "data": "created_on" },
                        ]
                    });
                }
                else if(json[0].hasOwnProperty("agentLoginName"))
                {
                    table = $('table#tableID2').DataTable({
                        "destroy": true,
                        "paging": true,
                        "processing": true,
                        "data": dataSet,
                        "columns": [
                            { "data": "engagementId" },
                            { "data": "startTime" },
                        ]
                    });
                }

                $('table#tableID2 tbody').on('click', 'tr', function () {
                    //use this code to go down to the state level
                    //   var data = table.row( this ).data();
                    console.log(data);
                    //   var sessionID = data["engagementId"];
                    //   var sessionViewURL = "http://127.0.0.1:5000/conversations/" + sessionID;
                    //   window.open (sessionViewURL,'_self',false)
                })
            }
        })
    });
});
