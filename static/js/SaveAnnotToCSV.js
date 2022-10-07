/*
This script saves the annotated htlm table to a csv file;
ToDo: 
- modify app.py, 
- add warning message,
- incorporate in template html  
*/ 


// $("button").click(function(){
//     $.get("demo_test.asp", function(data, status){
//       alert("Data: " + data + "\nStatus: " + status);
//     });
//   });
//   $("button").click(function(){
//     $.post("demo_test_post.asp",
//     {
//       name: "Donald Duck",
//       city: "Duckburg"
//     },
//     function(data, status){
//       alert("Data: " + data + "\nStatus: " + status);
//     });
//   });


// let input_data;
// $.ajax({
//   type: "GET",  
//   url: "static/data/data.csv",
//   dataType: "text",       
//   success: function(response)  
//   {
//     input_data = $.csv.toArrays(response);
//     // generateHtmlTable(data);
//     alert("Data saved successfully");
//   },  
//   error: function(){
//     alert("Failed to save data")
// }
// });
/*
$.ajax({
  type: "POST",
  url: "/process_qtc",
  data: JSON.stringify(server_data),
  contentType: "application/json",
  dataType: 'json' 
});
@app.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation():
  if request.method == "POST":
    qtc_data = request.get_json()
    print(qtc_data)
*/