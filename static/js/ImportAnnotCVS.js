
let input_data;
$.ajax({
  type: "GET",  
  url: "static/data/data.csv",
  dataType: "text",       
  success: function(response)  
  {
    input_data = $.csv.toArrays(response);
    // generateHtmlTable(data);
    alert("Data saved successfully");
  },  
  error: function(){
    alert("Failed to save data")
}
});