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

var saveData =$.ajax({
    url: dest_data_dir,
    cache: false,
    contentType: "json; charset=UTF-8",
    data: annot_data,
    type: "POST",
    success: function(resultData){
          alert("Data saved successfully");
      }, //need to change the success function
    error: function(){
        alert("Failed to save data")
    } //need to change the failure function
});

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