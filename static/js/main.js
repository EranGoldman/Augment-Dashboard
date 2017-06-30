// fs = require('fs');




$(document).ready(function() {
    $.getJSON("http://127.0.0.1:5000/conversations", function(json) {
        console.log(json);

        var dataSet = json;


        $('table#tableID').DataTable({
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


        // var localData = json;
        // var tr;
        // for (var i = 0; i < json.length; i++) {
        //     tr = $('<tr/>');
        //     tr.append("<td>" + json[i].agentFullName + "</td>");
        //     tr.append("<td>" + json[i].engagementId + "</td>");
        //     tr.append("<td>" + json[i].chatLines + "</td>");
        //     $('table#tableID').append(tr);
        // }



        // $.ajax({
        //     url: "https://reqres.in/api/users?page=2"
        // }).then(function(serverpull) {
        //     // console.log(serverpull);
        //     var temp = serverpull;
        //     var data1 = temp.total_pages;
        //     var data2 = temp.total;
        //     var data3 = temp.per_page;
        //     var data4 = temp.per_page;
        //     $('.fridge-chats').append(data1);
        //     $('.augmented-chats').append(data2);
        //
        //     console.log(localData[0].message_id);
        //     var data = {
        //         labels: ["MON", "TUE", "WED", "THR", "FRI", "SAT", "SUN"],
        //         datasets: [
        //             {
        //                 label: "Augmented Chats",
        //                 fillColor: "#eb4267",
        //                 strokeColor: "white",
        //                 pointColor: "white",
        //                 pointStrokeColor: "#eb4267",
        //                 pointHighlightFill: "#eb4267",
        //                 pointHighlightStroke: "#eb4267",
        //                 data: [165, 159, 180, 181, 156, 155, localData[0].message_id]
        //             }
        //         ]
        //     }
        //     var ctx = new Chart(document.getElementById("myChart").getContext("2d")).Line(data);
    });
});





//
//
// function drawLineChart() {
//     // Add a helper to format timestamp data
//     Date.prototype.formatMMDDYYYY = function() {
//         return (this.getMonth() + 1) +
//         "/" +  this.getDate() +
//         "/" +  this.getFullYear();
//     }
//
//     var jsonData = $.ajax({
//         url: 'http://rest-service.guides.spring.io/greeting',
//         dataType: 'json',
//     }).done(function (results) {
//
//         // Split timestamp and data into separate arrays
//         var labels = [], data=[];
//         $('.greeting-id').append(data.id);
//         $('.greeting-content').append(data.content);
//         labels.push(results.content);
//         data.push(results.id);
//     );
//
//     // Create the chart.js data structure using 'labels' and 'data'
//     var tempData = {
//         labels : labels,
//         datasets : [{
//             fillColor             : "rgba(151,187,205,0.2)",
//             strokeColor           : "rgba(151,187,205,1)",
//             pointColor            : "rgba(151,187,205,1)",
//             pointStrokeColor      : "#fff",
//             pointHighlightFill    : "#fff",
//             pointHighlightStroke  : "rgba(151,187,205,1)",
//             data                  : data
//         }]
//     };
//
//     // Get the context of the canvas element we want to select
//     var ctx = document.getElementById("myLineChart").getContext("2d");
//
//     // Instantiate a new chart
//     var myLineChart = new Chart(ctx).Line(tempData, {
//         //bezierCurve: false
//     });
// });
// }
//
// drawLineChart();
