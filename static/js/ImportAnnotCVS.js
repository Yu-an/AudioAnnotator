var importData =$.ajax({
    url: scr_data_dir,
    cache: false,
    contentType: "json; charset=UTF-8",
    // data: input_data,
    type: "GET",
    success: function(resultData){
          alert("Data import Complete");
      }, //need to change the success function
    error: function(){
        alert("Import data failed")
    } //need to change the failure function
});